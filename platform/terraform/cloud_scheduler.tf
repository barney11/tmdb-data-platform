resource "google_cloud_scheduler_job" "tmdb_data_workflow_scheduler" {
  name        = "tmdb-data-workflow-scheduler"
  description = "Workflow scheduler for movies data processing."
  schedule    = "0 9 * * *"  # Trigger at 9:00 AM every day (UTC time)

  http_target {
    http_method = "GET"
    uri         = "https://workflowexecutions.googleapis.com/v1/projects/movies-data-platform/locations/us-central1/workflows/tmdb-workflow/executions"
  }

  time_zone = "Europe/Paris"

  retry_config {
    retry_count = 3
  }
}
