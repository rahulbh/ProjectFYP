// validator.js
//   An example of input validation using the input, using the DOM 2 event model
//   Note: This document does not work with IE8

// ********************************************************** //
// The event handler function for the name text box

function chkPass(event) {

// Get the target node of the event

  var myPass = event.currentTarget;

// Test the format of the input name 
//  Allow the spaces after the commas to be optional
//  Allow the period after the initial to be optional

  var pos = myPass.value.search(/^[A-Za-z\d]{4,}/);

  if (pos != 0) {
    alert("The password you entered is not in the correct form. Atleast 4 chars \n");
    myPass.focus();
    myPass.select();
	return false;
  } 
}

// ********************************************************** //
// The event handler function for the phone number text box

function chkMail(event) {

// Get the target node of the event

  var myMail = event.currentTarget;

// Test the format of the input name 
//  Allow the spaces after the commas to be optional
//  Allow the period after the initial to be optional

  var pos = myMail.value.search(/^[\w.-]+@[\w.-]+\.[A-Za-z]{2,3}$/);

  if (pos != 0) {
    alert("The Email ID you entered (" + myMail.value + 
          ") is not in the correct form. \n" +
          "The correct form is: " +
          "john@gmail.com ");
    myMail.focus();
    myMail.select();
   return false;
  } 
}



