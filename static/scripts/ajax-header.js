htmx.defineExtension('ajax-header', {
    onEvent: function (name, evt) {
        if (name === "htmx:configRequest") {
            evt.detail.headers['bypass-tunnel-reminder'] = 'true';
        }
    }
});