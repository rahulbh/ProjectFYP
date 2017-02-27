// validator2r.js
//   The last part of validator2. Registers the 
//   event handlers
//   Note: This script does not work with IE8

// Get the DOM addresses of the elements and register 
//  the event handlers

      var mailNode = document.getElementById("mailid");
      var passNode = document.getElementById("pass");
      
      mailNode.addEventListener("submit", chkMail, false);
      passNode.addEventListener("submit", chkPass, false);

