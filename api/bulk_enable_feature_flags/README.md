# Bulk Enable Course Feature Flags

## Summary

This script utilizes a CSV file to update the state of course feature flags in bulk.

## Setup

**[bulk-enable-feature-flags.rb](bulk-enable-feature-flags.rb)**

- `feature`
  - The actual feature flag to toggle
  - EX: `student_outcome_gradebook`
  - Use this API request to GET available feature flags => <https://canvas.instructure.com/doc/api/feature_flags.html#method.feature_flags.index>

**[courses.csv](courses.csv)**

Your CSV file should contain the following headers:

- `course_id`
  - value expected - integer
  - The ID will be the ID from the course's Canvas URL
  - EX: `https://<YOUR_DOMAIN>.instructure.com/courses/<course_id>`
- `status`
  - value expected - "off" or "on"

## NOTE

**Features may be locked on the Account level!**

> Depending on the local settings for feature flags on the account level, your Canvas admins may have "locked" the status of feature flags within a course. If this is the case, you'll see an italicized status for a feature flag instead of a toggle switch.
