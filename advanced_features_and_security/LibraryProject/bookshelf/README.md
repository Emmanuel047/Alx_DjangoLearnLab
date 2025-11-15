# Permissions and Groups Setup for Bookshelf App

## Custom Permissions
Defined on the `Book` model:
- can_view
- can_create
- can_edit
- can_delete

## Groups and Permissions
- Viewers: can_view
- Editors: can_view, can_create, can_edit
- Admins: can_view, can_create, can_edit, can_delete

## Views
Protected with `@permission_required` decorator enforcing permission checks.

## Usage
Assign users to groups in admin to control access, ensuring secure and role-based permission handling.
