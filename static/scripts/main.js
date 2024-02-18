document.addEventListener('alpine:init', () => {
    Alpine.store('tab', {
        activeTab: false,

        getActiveStatus(id) {
            return id === this.activeTab
        }
    })
})