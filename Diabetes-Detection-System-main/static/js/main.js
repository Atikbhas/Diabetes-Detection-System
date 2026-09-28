// ==============================================================================
// MAIN CLIENT-SIDE SCRIPT — DIABETES DETECTION SYSTEM (DDS)
// ==============================================================================
// Client-side JavaScript code. Handles BMI calculation, form focus guidance sync,
// form submit loading spinner ane alert auto-dismiss mate functionality cover kare chhe.
// ==============================================================================

document.addEventListener('DOMContentLoaded', function () {
    // --------------------------------------------------------------------------
    // 1. BMI INTERACTIVE CALCULATOR WIDGET LOGIC
    // Height (cm) ane Weight (kg) par thi BMI calculate kari prediction form ma auto-fill karse.
    // --------------------------------------------------------------------------
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
                // Highlight filled input smoothly
                bmiInput.classList.add('is-valid', 'border-success');
                setTimeout(() => bmiInput.classList.remove('is-valid', 'border-success'), 2000);
            }
        });
    }

    // --------------------------------------------------------------------------
    // 2. FIELD FOCUS GUIDANCE SYNC (Smooth internal sidebar scroll)
    // Form input focus thaye tyare corresponding guidance card active thase.
    // Main page ma koi lag vager internal sidebar ma smoothly scroll thase.
    // --------------------------------------------------------------------------
    const inputs = document.querySelectorAll('.medical-input');
    const guidanceCards = document.querySelectorAll('.guidance-card');
    const sidebar = document.querySelector('.guidance-sidebar');

    inputs.forEach(input => {
        input.addEventListener('focus', function () {
            const fieldName = this.dataset.guidanceKey || this.name;
            const guidanceCard = document.getElementById(`guidance-${fieldName}`);
            if (guidanceCard) {
                guidanceCards.forEach(c => c.classList.remove('active-guidance'));
                guidanceCard.classList.add('active-guidance');
                
                // Smoothly scroll ONLY the internal sidebar container without forcing window reflow
                if (sidebar) {
                    const cardTop = guidanceCard.offsetTop - sidebar.offsetTop - 10;
                    sidebar.scrollTo({ top: Math.max(0, cardTop), behavior: 'smooth' });
                }
            }
        });

        // Mouse wheel scroll thi number values accidental change na thaye te mate blur handler.
        input.addEventListener('wheel', function (e) {
            if (document.activeElement === this) {
                this.blur();
            }
        });
    });

    // --------------------------------------------------------------------------
    // 3. FORM SUBMIT BUTTON LOADING STATE & DOUBLE-CLICK PREVENTION
    // Form submit karta j submit button disable thase ane spinner show thase.
    // --------------------------------------------------------------------------
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function () {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn && !submitBtn.disabled) {
                submitBtn.disabled = true;
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = `<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Processing...`;
            }
        });
    });

    // --------------------------------------------------------------------------
    // 4. AUTO-DISMISS FLASH ALERTS
    // Success/warning flash alerts 5 seconds pachi automatic hide thai jase.
    // --------------------------------------------------------------------------
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (window.bootstrap && bootstrap.Alert) {
                const bsAlert = bootstrap.Alert.getInstance(alert) || new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 5000);
    });
});

