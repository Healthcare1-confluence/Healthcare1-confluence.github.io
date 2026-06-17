# Appointment Scheduler Agent

Specialist agent for appointment lifecycle management.

## Tools

- `get_available_slots` — Fetch available slots by date
- `validate_appointment_slot` — Verify slot availability
- `book_appointment` — Create appointment with pre-auth check
- `reschedule_appointment` — Update existing appointment
- `cancel_appointment` — Release slot
- `get_slots_for_range` — Fetch slots across date range
- `get_earliest_available_slot` — Find next available slot
- `get_member_appointments` — Retrieve upcoming appointments

## Pre-Authorization

All bookings validated against pre_auth table. Restricts to authorized providers.

