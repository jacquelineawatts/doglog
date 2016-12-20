"use strict";

$(function() {
    $("#signupForm").validate({
        rules: {
            first_name: 'required',
            last_name: 'required',
            email:  {
                required: true,
                email: true
            },
            password: {
                required: true,
                minlength: 8,
            }
        },
        messages: {
            first_name: "Please enter your first name.",
            last_name: "Please enter your last name.",
            email: "Please enter a valid email address.",
            password: "Your password must be at least 8 characters long.",
        },
        submitHandler: function(form) {
            form.submit();
        }
    });
});

$(function() {
    $("#loginForm").validate({
        rules: {
            email:  {
                required: true,
                email: true
            },
        },
        messages: {
            email: "Please enter a valid email address.",
        },
        submitHandler: function(form) {
            form.submit();
        }
    });
});



