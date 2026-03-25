// disable obfuscate button on query
const button = document.getElementById("obfuscateButton");
document.body.addEventListener('htmx:configRequest', function() {
    button.disabled = true;
});
document.body.addEventListener('htmx:afterOnLoad', function() {
    button.disabled = false;
});
document.body.addEventListener('htmx:responseError', function() {
    button.disabled = false;
});

// copy the output to clipboard
document.getElementById("copyButton").onclick = function() {
    const content = document.getElementById("output").innerText.trimEnd();
    navigator.clipboard.writeText(content).catch(err => {
        console.error("Failed to copy: ", err);
    });

    // show copied toast
    const toast = document.getElementById("toast");
    toast.classList.remove("hidden");
    setTimeout(() => {
        toast.classList.add("hidden");
    }, 600);
};

class AdvanceOptionsDrawer {
    constructor() {
        this.drawer = document.getElementById("advancedOptionsDrawer");
        this.drawerToggle = document.getElementById("advancedOptionsDrawerToggle");
        this.unselectAllBtn = document.getElementById("unselectAllButton");

        this.toggleDrawer = this.toggleDrawer.bind(this);
        this.closeDrawer = this.closeDrawer.bind(this);

        this.attachEventListeners();
    }

    attachEventListeners() {
        this.drawerToggle.addEventListener("click", this.toggleDrawer);
        this.unselectAllBtn.addEventListener("click", () => this.setAllCheckboxes(false));
    }

    setAllCheckboxes(checked) {
        const form = this.drawer.closest("form");
        form.querySelectorAll('input[type="checkbox"]:not(:disabled)').forEach(cb => {
            cb.checked = checked;
        });
    }

    toggleDrawer() {
        this.drawer.classList.toggle("hidden");
    }

    closeDrawer() {
        this.drawer.classList.add("hidden");
    }
}

document.addEventListener("DOMContentLoaded", () => {
    new AdvanceOptionsDrawer();
});
