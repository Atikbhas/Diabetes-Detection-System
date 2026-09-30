// Main Client-side Script for Diabetes Detection System (DDS)

document.addEventListener('DOMContentLoaded', function () {
    // 1. BMI Interactive Calculator Widget Logic
    const calcBtn = document.getElementById('calc-bmi-btn');
    if (calcBtn) {
        calcBtn.addEventListener('click', function () {
            const heightCm = parseFloat(document.getElementById('height-cm').value);
            const weightKg = parseFloat(document.getElementById('weight-kg').value);
            const bmiResultBox = document.getElementById('bmi-calc-result');
            const bmiInput = document.getElementById('bmi');

            if (!heightCm || !weightKg || heightCm <= 0 || weightKg <= 0) {
                bmiResultBox.innerHTML = '<span class="text-danger small"><i class="bi bi-exclamation-triangle"></i> Please enter valid positive values for height and weight.</span>';
                return;
            }

            // Formula: Weight (kg) / (Height (m))^2
            const heightM = heightCm / 100.0;
            const bmi = weightKg / (heightM * heightM);
            const roundedBMI = bmi.toFixed(1);

            let status = 'Normal weight';
            let badgeClass = 'text-success';
            if (bmi < 18.5) {
                status = 'Underweight';
                badgeClass = 'text-warning';
            } else if (bmi >= 25.0 && bmi < 30.0) {
                status = 'Overweight';
                badgeClass = 'text-warning';
            } else if (bmi >= 30.0) {
                status = 'Obese';
                badgeClass = 'text-danger';
            }

            bmiResultBox.innerHTML = `Calculated BMI: <strong>${roundedBMI} kg/m²</strong> (<span class="${badgeClass}">${status}</span>). Auto-filled into prediction form!`;

            if (bmiInput) {
                bmiInput.value = roundedBMI;
                // Highlight filled input
                bmiInput.classList.add('is-valid');
                setTimeout(() => bmiInput.classList.remove('is-valid'), 2000);
            }
        });
    }

    // 2. Field Focus Guidance Focus Sync
    const inputs = document.querySelectorAll('.medical-input');
    inputs.forEach(input => {
        input.addEventListener('focus', function () {
            const fieldName = this.dataset.guidanceKey || this.name;
            const guidanceCard = document.getElementById(`guidance-${fieldName}`);
            if (guidanceCard) {
                // Remove existing highlights
                document.querySelectorAll('.guidance-card').forEach(c => c.classList.remove('border-primary', 'shadow'));
                guidanceCard.classList.add('border-primary', 'shadow');
                guidanceCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
        });
    });

    // 3. Auto-dismiss flash alerts
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});
