document.addEventListener('DOMContentLoaded', function() {
    function clearAllData() {
        const forms = [patientForm, binaryForm, multiForm, reportForm];
        forms.forEach(form => {
            if (form) form.reset();  // Clear all forms
        });

        const hiddenInputs = document.querySelectorAll('input[type="hidden"]');
        hiddenInputs.forEach(input => {
            input.value = '';  // Reset all hidden input values
        });

        const resultSections = document.querySelectorAll('.result-section');
        resultSections.forEach(section => {
            section.style.display = 'none';  // Hide result sections
        });

        const predictionTexts = document.querySelectorAll('#binaryPrediction, #multiPrediction');
        predictionTexts.forEach(text => {
            text.textContent = '';  // Clear prediction text
        });

        const images = document.querySelectorAll('#binaryImage, #multiImage');
        images.forEach(img => {
            img.src = '';  // Clear image source
            img.style.display = 'none';  // Hide images
        });
    }

    clearAllData();  // Clear all data when the page is loaded

    window.addEventListener('pageshow', function(event) {
        if (event.persisted || (window.performance && window.performance.navigation.type === 2)) {
            clearAllData();  // Clear all data when page is restored from cache
        }
    });

    if (performance.getEntriesByType('navigation')[0].type === 'reload') {
        clearAllData();  // Clear all data on page reload (hard refresh)
    }
    
});
