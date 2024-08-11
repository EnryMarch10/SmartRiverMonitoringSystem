document.addEventListener('DOMContentLoaded', (event) => {
    const manualForm = document.getElementById('manual-form')
    const currentModeLabel = document.getElementById('system-modality').children[0]
    if (currentModeLabel.textContent == 'AUTOMATIC') {
        manualForm.style.display = 'none'
    } else {
        manualForm.style.display = 'block'
    }
})

function toggleModality() {
    const buttonToggleModality = document.getElementById('toggle-mode');
    buttonToggleModality.disabled = true

    const currentModeLabel = document.getElementById('system-modality').children[0]
    let nextModality
    if (currentModeLabel.textContent === 'AUTOMATIC') {
        nextModality = 'MANUAL'
    } else {
        nextModality = 'AUTOMATIC'
    }
    $.ajax({
        url: '/toggle_modality',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            mode: nextModality
        }),
        success: function (response) {
            if (response.result == 'OK') {
                const manualForm = document.getElementById('manual-form')
                if (currentModeLabel.textContent === 'AUTOMATIC') {
                    currentModeLabel.textContent = 'MANUAL'
                    manualForm.style.display = 'block'
                } else {
                    currentModeLabel.textContent = 'AUTOMATIC'
                    manualForm.style.display = 'none'
                }
            } else {
                window.alert('Error occurred in toggling modality, probably someone is using the other mode, retry in some time')
            }
        },
        error: function (response) {
            console.error('Error toggling modality:', response);
        },
        complete: function() {
            buttonToggleModality.disabled = false
        }
    });
}

function submitValveLevel(event) {
    event.preventDefault()
    const valveLevelInput = document.getElementById('input-valve-level')
    const submitValveLevel = document.getElementById('set-valve-level')
    submitValveLevel.disabled = true
    $.ajax({
        url: '/set_valve_level',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            valve_level: valveLevelInput.value
        }),
        success: function (response) {
            if (response.result == 'OK') {
                const valveLevelValue = document.getElementById('valve-level').children[0]
                valveLevelValue.textContent = `${valveLevelInput.value} %`;
            } else {
                window.alert('Error occurred in setting valve level')
            }
        },
        error: function (response) {
            console.error('Error sending valve level:', response);
        },
        complete: function() {
            submitValveLevel.disabled = false
        }
    });
}
