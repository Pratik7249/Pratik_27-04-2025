# app/scripts/report_logic.py

import os
import pandas as pd
import pytz
import re  # ✅ Make sure this is imported at the top
from datetime import datetime, timedelta
from app.db.database import SessionLocal
from app.db.models import StoreStatus, BusinessHours, Timezones
from sqlalchemy import inspect

def generate_report(report_id: str = "store_uptime_report"):
    db = SessionLocal()

    try:
        # Confirm tables exist
        inspector = inspect(db.bind)
        print("Existing tables:", inspector.get_table_names())

        # Fetch store IDs
        store_ids = db.query(StoreStatus.store_id).distinct().all()
        store_ids = [s[0] for s in store_ids]

        # ⚡️ Filter only valid UUID store_ids (remove integer ones like 1, 10, etc.)
        uuid_regex = re.compile(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')
        store_ids = [store_id for store_id in store_ids if isinstance(store_id, str) and uuid_regex.match(store_id)]

        # Print total number of valid stores
        print(f"\n🔢 Total number of valid UUID stores found: {len(store_ids)}\n")

        if not store_ids:
            print("⚠️ No stores found in database.")
            return

        # Get current UTC reference time
        now_record = db.query(StoreStatus.timestamp_utc).order_by(StoreStatus.timestamp_utc.desc()).first()
        now_utc = now_record[0].replace(tzinfo=pytz.UTC) if now_record and now_record[0] else datetime.utcnow().replace(tzinfo=pytz.UTC)

        report_rows = []

        # Limit processing to first 10 stores
        for store_id in store_ids[:10]:
            print(f"🔄 Processing store {store_id}...")

            # 1. Timezone
            tz_row = db.query(Timezones).filter(Timezones.store_id == store_id).first()
            timezone_str = tz_row.timezone_str if tz_row else 'America/Chicago'
            try:
                tz = pytz.timezone(timezone_str)
            except pytz.UnknownTimeZoneError:
                tz = pytz.timezone('America/Chicago')

            # 2. Business Hours
            bh_rows = db.query(BusinessHours).filter(BusinessHours.store_id == store_id).all()
            if bh_rows:
                business_hours = {
                    row.day_of_week: (row.start_time_local, row.end_time_local) for row in bh_rows
                }
            else:
                business_hours = {i: ('00:00:00', '23:59:59') for i in range(7)}  # Assume 24x7 open

            # 3. Store Status
            statuses = db.query(StoreStatus).filter(StoreStatus.store_id == store_id).all()
            if not statuses:
                continue

            statuses_df = pd.DataFrame(
                [(s.timestamp_utc, s.status) for s in statuses],
                columns=['timestamp_utc', 'status']
            )
            statuses_df['timestamp_utc'] = pd.to_datetime(statuses_df['timestamp_utc'], utc=True)
            statuses_df = statuses_df.sort_values('timestamp_utc')

            def calculate_uptime_downtime(start_time_utc, end_time_utc):
                total_minutes = int((end_time_utc - start_time_utc).total_seconds() / 60)
                if statuses_df.empty:
                    return 0, total_minutes

                timeline = pd.date_range(start=start_time_utc, end=end_time_utc - timedelta(minutes=1), freq='1min', tz=pytz.UTC)
                timeline_df = pd.DataFrame({'timestamp_utc': timeline})

                timeline_df = pd.merge_asof(
                    timeline_df,
                    statuses_df,
                    on='timestamp_utc',
                    direction='backward',
                    tolerance=pd.Timedelta('1D')
                )

                timeline_df['status'] = timeline_df['status'].fillna('inactive')

                timeline_df['timestamp_local'] = timeline_df['timestamp_utc'].dt.tz_convert(tz)
                timeline_df['day_of_week'] = timeline_df['timestamp_local'].dt.dayofweek
                timeline_df['time_local'] = timeline_df['timestamp_local'].dt.time

                def within_hours(row):
                    day = row['day_of_week']
                    time = row['time_local']
                    if day not in business_hours:
                        return False
                    start_time = datetime.strptime(business_hours[day][0], '%H:%M:%S').time()
                    end_time = datetime.strptime(business_hours[day][1], '%H:%M:%S').time()
                    return start_time <= time <= end_time

                timeline_df['within_hours'] = timeline_df.apply(within_hours, axis=1)
                timeline_df = timeline_df[timeline_df['within_hours']]

                uptime = timeline_df[timeline_df['status'] == 'active'].shape[0]
                downtime = timeline_df[timeline_df['status'] == 'inactive'].shape[0]

                return int(uptime), int(downtime)

            # Calculate metrics
            uptime_last_hour, downtime_last_hour = calculate_uptime_downtime(now_utc - timedelta(hours=1), now_utc)
            uptime_last_day, downtime_last_day = calculate_uptime_downtime(now_utc - timedelta(days=1), now_utc)
            uptime_last_week, downtime_last_week = calculate_uptime_downtime(now_utc - timedelta(weeks=1), now_utc)

            report_rows.append({
                'store_id': store_id,
                'uptime_last_hour(min)': uptime_last_hour,
                'downtime_last_hour(min)': downtime_last_hour,
                'uptime_last_day(min)': uptime_last_day,
                'downtime_last_day(min)': downtime_last_day,
                'uptime_last_week(min)': uptime_last_week,
                'downtime_last_week(min)': downtime_last_week,
            })

        # Save to CSV
        os.makedirs('output', exist_ok=True)
        df_report = pd.DataFrame(report_rows)
        output_file = os.path.join('output', f'{report_id}.csv')
        df_report.to_csv(output_file, index=False)
        print(f"\n✅ Report generated at {output_file}")

    finally:
        db.close()

if __name__ == "__main__":
    generate_report()
