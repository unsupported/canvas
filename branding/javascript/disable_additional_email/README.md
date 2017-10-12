# Remove the Option for all users to Add Additional Email

This will remove the option to add an additional email address, hiding both the "+Email Address" and the "Email" tab within the "Register Communication" modal.  Adding a contact method, or "Text (SMS)", will still be available.

Optional lines have been added to remove the ability to add a phone number ("+Contact Method") as well and can be removed if not applicable.

# Edits to Make Prior to Using

Two separate blocks of javascript make up the `hide_additionalEmail.js` file, each blocking separate items.  You'll need to remove the block not applicable to your needs.
