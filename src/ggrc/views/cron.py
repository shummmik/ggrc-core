# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

""" Cron job endpoints initialization and running stuff """

from logging import getLogger
from traceback import format_exc

from ggrc import extensions
from ggrc.notifications import common
from ggrc.integrations import synchronization_jobs
from ggrc.integrations.synchronization_jobs.assessment_sync_job import test_sync_assessment_attributes

# pylint: disable=invalid-name
logger = getLogger(__name__)


def send_error_notification(message):
  try:
    user_email = common.get_app_engine_email()
    common.send_email(user_email, "Error in nightly cron job", message)
  except:  # pylint: disable=bare-except
    logger.exception("Failed on sending notification")


def run_job(job):
  """Call sent job.

  Failuare on job will just logged and don't stop runner.
  """
  try:
    job()
  except:  # pylint: disable=bare-except
    logger.exception("Job '%s' failed", job.__name__)
    send_error_notification(
        "Job '%s' failed with: \n%s" % (job.__name__, format_exc())
    )


def job_runner(name):
  """Run all contributed jobs from all extension modules"""
  cron_jobs = extensions.get_module_contributions(name)
  for job in cron_jobs:
    run_job(job)
  return 'Ok'


def nightly_cron_endpoint():
  """Endpoint running nightly jobs from all modules"""
  return job_runner("NIGHTLY_CRON_JOBS")


def hourly_issue_tracker_sync_endpoint():
  """Endpoint running hourly jobs from all modules"""
  return job_runner("HOURLY_CRON_JOBS")


def sync_assessment_attributes():
  """Endpoint running assessment attributes synchronization."""
  print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
  return  # synchronization_jobs.sync_assessment_attributes()


def sync_issue_attributes():
  """Endpoint running issue attributes synchronization."""
  return synchronization_jobs.sync_issue_attributes()


def sync_my_attributes():
  """Endpoint running issue attributes synchronization."""
  return test_sync_assessment_attributes()


def half_hour_cron_endpoint():
  """Endpoint running half hourly jobs from all modules"""
  return job_runner("HALF_HOUR_CRON_JOBS")


def init_cron_views(app):
  """Init all cron jobs' endpoints"""
  app.add_url_rule(
      "/nightly_cron_endpoint", "nightly_cron_endpoint",
      view_func=nightly_cron_endpoint)

  app.add_url_rule(
      "/hourly_issue_tracker_sync_endpoint",
      "hourly_issue_tracker_sync_endpoint",
      view_func=hourly_issue_tracker_sync_endpoint
  )

  app.add_url_rule(
      "/half_hour_cron_endpoint", "half_hour_cron_endpoint",
      view_func=half_hour_cron_endpoint
  )

  app.add_url_rule(
      "/sync_assessment_attributes"
      "sync_assessment_attributes",
      view_func=sync_assessment_attributes
  )

  app.add_url_rule(
      "/sync_issue_attributes"
      "sync_issue_attributes",
      view_func=sync_issue_attributes
  )
  # raise Exception
  app.add_url_rule(
    "/sync_my_attributes"
    "sync_my_attributes",
    view_func=sync_my_attributes
  )
