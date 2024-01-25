const password = document.getElementById('password');
const confirm_password = document.getElementById('confirm_password');
const registration_submit = document.getElementById('registration_submit');

//Event handler for form submission that verifies that the passwords match
registration_submit.addEventListener('click', (e) => {
    if (password.value != confirm_password.value) {
        //Passwords do not match
 
        //Set custom validity message
        password.setCustomValidity('Passwords do not match.');
        //Report validity
        password.reportValidity();
    } else {
        //Reset custom validity message so the form is able to proceed to submitting
        password.setCustomValidity('');
    }
});
