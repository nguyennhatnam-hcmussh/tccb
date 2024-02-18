htmx.defineExtension('bypass', {
    onEvent: function (name, evt) {
        if (name === "htmx:configRequest") {
            evt.detail.headers['bypass-tunnel-reminder'] = 'true';
        }
    }
});