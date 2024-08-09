document.addEventListener('DOMContentLoaded', (event) => {
    const manualForm = document.getElementById('manual-form')
    if (currentModeLabel.textContent === 'AUTOMATIC') {
        currentModeLabel.textContent = 'MANUAL'
        manualForm.style.display = 'block'
    } else {
        currentModeLabel.textContent = 'AUTOMATIC'
        manualForm.style.display = 'none'
    }
})

function toggleModality() {
    const manualForm = document.getElementById('manual-form')
    const currentModeLabel = document.getElementById('system-modality').children[0]
    if (currentModeLabel.textContent === 'AUTOMATIC') {
        currentModeLabel.textContent = 'MANUAL'
        manualForm.style.display = 'block'
    } else {
        currentModeLabel.textContent = 'AUTOMATIC'
        manualForm.style.display = 'none'
    }
    // TODO: tell to toggle modality
}

function submitValveLevel(event) {
    event.preventDefault()
    // TODO: tell to send new valve level
    // const valveLevelInput = document.getElementById('input-valve-level')
    // const valveLevelValue = document.getElementById('valve-level').children[0]
    // valveLevelValue.textContent = `${valveLevelInput.value} %`;
}
