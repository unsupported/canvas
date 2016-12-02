## Help Menu Tray Modifications

To edit the help menu tray in Canvas you need to set an event listener on the menu click. This JS snippet sets this listener and waits for the element to render to make changes to the element.

The elements in the tray are rendered on click. This snippet sets the listener for the help menu click, but it does not set a listener for the "cancel" button on the report a problem form. To reduce complexity I've just opted to remove this button via CSS, users can still exit the menu by clicking on the overlay or closing X.