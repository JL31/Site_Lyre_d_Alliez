$(function ()
{
    /* Fonctions */
    /* --------- */

    let chargementFormulaireDemandeDevenirSoutien = function()
    {
        let btn = $(this);

        $.ajax(
        {
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function ()
            {
                $("#modal-devenir-soutien").modal("show");
            },
            success: function (data)
            {
                $("#modal-devenir-soutien .modal-content").html(data.html_form);
            }
        });
    };

    let sauvegardeFormulaireDemandeDevenirSoutien = function()
    {
        let form = $(this);

        $.ajax(
        {
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data)
            {
                if (data.form_is_valid)
                {
                    alert("Terminé !");
                    $("#modal-devenir-soutien").modal("hide");
                }
                else
                {
                    $("#modal-devenir-soutien .modal-content").html(data.html_form);
                }
            }
        });

        return false;

    };

    /* Liens */
    /* ----- */

    $(".js-demande-pour-devenir-soutien").click(chargementFormulaireDemandeDevenirSoutien);
    $("#modal-devenir-soutien").on("submit", ".js-demande-pour-devenir-soutien-creation-formulaire", sauvegardeFormulaireDemandeDevenirSoutien);
});
