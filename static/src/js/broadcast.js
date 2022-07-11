odoo.define("web_company_logo.Menu", function (require) {
  "use strict";

  var session = require("web.session");
  var Menu = require("web.Menu");

  Menu.include({
    /**
     * @override
     */
    start: function (parent, options) {
      this._super.apply(this, arguments);

      var url = window.location.origin;
      var companyId = session.company_id;
      $.ajax({
        type: "GET",
        data: { company_id: companyId },
        url: `${url}/broadcast`,
        success: function (result) {
          var result = JSON.parse(result);
          const element = document.getElementById("broadcast-alert");
          let notifAlert = `
            <div class="alert alert-${result.type_notification} alert-dismissible fade show" role="alert">
              <p>${result.description}</p>
              <button type="button" class="close" data-dismiss="alert" aria-label="Close">×</button>
            </div>
            `;

          if (result.description) {
            element.innerHTML = notifAlert;
          } else {
            $("#broadcast-alert")[0].remove();
          }
        },
        error: function (xhr, ajaxOptions, thrownError) {
          console.log("Error encountered");
        },
      });
    },
  });
});
