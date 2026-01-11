"""Oura sync module."""

import logging
from datetime import date, timedelta, datetime
from .oura_db import (Profile, DailySleep, DailyActivity, DailyReadiness, HeartRate,
                      Session, Workout, Tag, SpO2, Stress, RingConfiguration, HeartHealth)

logger = logging.getLogger(__name__)

def sync_data(client, db_manager, start_date=None, end_date=None):
    if not start_date:
        start_date = date.today() - timedelta(days=7)
    if not end_date:
        end_date = date.today()

    logger.info(f"Syncing data from {start_date} to {end_date}")

    with db_manager.managed_session() as session:
        # Profile
        logger.info("Syncing Profile...")
        try:
            profile_data = client.get_personal_info()
            if profile_data:
                profile = Profile(
                    id=profile_data.get('id'),
                    email=profile_data.get('email'),
                    weight=profile_data.get('weight'),
                    height=profile_data.get('height'),
                    age=profile_data.get('age'),
                    biological_sex=profile_data.get('biological_sex')
                )
                session.merge(profile)
        except Exception as e:
            logger.error(f"Failed to sync profile: {e}")

        # Daily Sleep
        logger.info("Syncing Daily Sleep...")
        sleeps = client.get_daily_sleep(start_date, end_date)
        if sleeps and 'data' in sleeps:
            for item in sleeps['data']:
                daily_sleep = DailySleep(
                    id=item.get('id'),
                    day=datetime.strptime(item.get('day'), '%Y-%m-%d').date(),
                    score=item.get('score'),
                    contributors=item.get('contributors'),
                    timestamp=datetime.fromisoformat(item.get('timestamp').replace('Z', '+00:00')) if item.get('timestamp') else None
                )
                session.merge(daily_sleep)

        # Daily Activity
        logger.info("Syncing Daily Activity...")
        activities = client.get_daily_activity(start_date, end_date)
        if activities and 'data' in activities:
            for item in activities['data']:
                daily_activity = DailyActivity(
                    day=datetime.strptime(item.get('day'), '%Y-%m-%d').date(),
                    score=item.get('score'),
                    active_calories=item.get('active_calories'),
                    average_met=item.get('average_met'),
                    contributers=item.get('contributors'),
                    equivalent_walking_distance=item.get('equivalent_walking_distance'),
                    high_activity_met_min=item.get('high_activity_met_min'),
                    high_activity_time=item.get('high_activity_time'),
                    inactivity_alerts=item.get('inactivity_alerts'),
                    low_activity_met_min=item.get('low_activity_met_min'),
                    low_activity_time=item.get('low_activity_time'),
                    medium_activity_met_min=item.get('medium_activity_met_min'),
                    medium_activity_time=item.get('medium_activity_time'),
                    met=item.get('met'),
                    meters_to_target=item.get('meters_to_target'),
                    non_wear_time=item.get('non_wear_time'),
                    resting_time=item.get('resting_time'),
                    sedentary_met_min=item.get('sedentary_met_min'),
                    sedentary_time=item.get('sedentary_time'),
                    steps=item.get('steps'),
                    target_calories=item.get('target_calories'),
                    target_meters=item.get('target_meters'),
                    total_calories=item.get('total_calories'),
                    timestamp=datetime.fromisoformat(item.get('timestamp').replace('Z', '+00:00')) if item.get('timestamp') else None
                )
                session.merge(daily_activity)

        # Daily Readiness
        logger.info("Syncing Daily Readiness...")
        readiness = client.get_daily_readiness(start_date, end_date)
        if readiness and 'data' in readiness:
            for item in readiness['data']:
                daily_readiness = DailyReadiness(
                    day=datetime.strptime(item.get('day'), '%Y-%m-%d').date(),
                    score=item.get('score'),
                    contributors=item.get('contributors'),
                    temperature_deviation=item.get('temperature_deviation'),
                    temperature_trend_deviation=item.get('temperature_trend_deviation'),
                    timestamp=datetime.fromisoformat(item.get('timestamp').replace('Z', '+00:00')) if item.get('timestamp') else None
                )
                session.merge(daily_readiness)

        # Heart Rate
        logger.info("Syncing Heart Rate...")
        hr_data = client.get_heartrate(start_date, end_date)
        if hr_data and 'data' in hr_data:
            for item in hr_data['data']:
                timestamp = datetime.fromisoformat(item.get('timestamp').replace('Z', '+00:00')) if item.get('timestamp') else None
                if timestamp:
                    hr = HeartRate(
                        timestamp=timestamp,
                        bpm=item.get('bpm'),
                        source=item.get('source')
                    )
                    session.merge(hr)

        # Sessions
        logger.info("Syncing Sessions...")
        sessions = client.get_sessions(start_date, end_date)
        if sessions and 'data' in sessions:
            for item in sessions['data']:
                session_obj = Session(
                    id=item.get('id'),
                    day=datetime.strptime(item.get('day'), '%Y-%m-%d').date(),
                    start_datetime=datetime.fromisoformat(item.get('start_datetime').replace('Z', '+00:00')) if item.get('start_datetime') else None,
                    end_datetime=datetime.fromisoformat(item.get('end_datetime').replace('Z', '+00:00')) if item.get('end_datetime') else None,
                    type=item.get('type'),
                    mood=item.get('mood'),
                    motion_count=item.get('motion_count')
                )
                session.merge(session_obj)

        # Workouts
        logger.info("Syncing Workouts...")
        workouts = client.get_workouts(start_date, end_date)
        if workouts and 'data' in workouts:
            for item in workouts['data']:
                workout = Workout(
                    id=item.get('id'),
                    day=datetime.strptime(item.get('day'), '%Y-%m-%d').date(),
                    start_datetime=datetime.fromisoformat(item.get('start_datetime').replace('Z', '+00:00')) if item.get('start_datetime') else None,
                    end_datetime=datetime.fromisoformat(item.get('end_datetime').replace('Z', '+00:00')) if item.get('end_datetime') else None,
                    activity=item.get('activity'),
                    calories=item.get('calories'),
                    distance=item.get('distance')
                )
                session.merge(workout)

        # Tags
        logger.info("Syncing Tags...")
        tags = client.get_tags(start_date, end_date)
        if tags and 'data' in tags:
            for item in tags['data']:
                tag = Tag(
                    id=item.get('id'),
                    day=datetime.strptime(item.get('day'), '%Y-%m-%d').date(),
                    text=item.get('text'),
                    timestamp=datetime.fromisoformat(item.get('timestamp').replace('Z', '+00:00')) if item.get('timestamp') else None,
                    tags=item.get('tags')
                )
                session.merge(tag)

         # SpO2
        logger.info("Syncing SpO2...")
        try:
             spo2_data = client.get_daily_spo2(start_date, end_date)
             if spo2_data and 'data' in spo2_data:
                for item in spo2_data['data']:
                    spo2 = SpO2(
                        day=datetime.strptime(item.get('day'), '%Y-%m-%d').date(),
                        average=item.get('average')
                    )
                    session.merge(spo2)
        except Exception as e:
            logger.warning(f"Failed to sync SpO2 (might not be available): {e}")

        # Stress
        logger.info("Syncing Stress...")
        stress_data = client.get_daily_stress(start_date, end_date)
        if stress_data and 'data' in stress_data:
            for item in stress_data['data']:
                stress = Stress(
                    day=datetime.strptime(item.get('day'), '%Y-%m-%d').date(),
                    stress_high=item.get('stress_high'),
                    recovery_high=item.get('recovery_high'),
                    day_summary=item.get('day_summary')
                )
                session.merge(stress)

        # Ring Configuration
        logger.info("Syncing Ring Configuration...")
        try:
            ring_data = client.get_ring_configuration(start_date, end_date)
            if ring_data and 'data' in ring_data:
                 for item in ring_data['data']:
                    ring = RingConfiguration(
                        id=item.get('id'),
                        color=item.get('color'),
                        design=item.get('design'),
                        firmware_version=item.get('firmware_version'),
                        hardware_type=item.get('hardware_type'),
                        model=item.get('model'),
                        size=item.get('size')
                    )
                    session.merge(ring)
        except Exception as e:
            # Ring config might be a single object or list, API docs vary
             logger.warning(f"Failed to sync Ring Config: {e}")

        # Heart Health
        logger.info("Syncing Heart Health...")
        try:
            hh_data = client.get_heart_health(start_date, end_date)
            if hh_data and 'data' in hh_data:
                for item in hh_data['data']:
                    hh = HeartHealth(
                        day=datetime.strptime(item.get('day'), '%Y-%m-%d').date(),
                        vascular_age=item.get('vascular_age')
                    )
                    session.merge(hh)
        except Exception as e:
             logger.warning(f"Failed to sync Heart Health: {e}")
