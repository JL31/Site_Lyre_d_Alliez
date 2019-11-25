$(function ()
{
    /* Fonctions */
    /* --------- */

    let chargementFormulaireAuthentification = function()
    {
        let element = $(this);

        $.ajax(
        {
            url: element.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function ()
            {
                $("#modal-authentification").modal("show");
            },
            success: function (data)
            {
                $("#modal-authentification .modal-content").html(data.html_form);
            }
        });
    };

    let sauvegardeFormulaireAuthentification = function()
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
                    if (data.user_authenticated)
                    {
                        $("#modal-authentification").modal("hide");
                        window.location.replace(data.url_pour_redirection);
                    }
                    else
                    {
                        alert("Le mot de passe est incorrect");
                        $("#id_mot_de_passe").val("");
                    }
                }
                else
                {
                    $("#modal-authentification .modal-content").html(data.html_form);
                }
            }
        });

        return false;

    };

    let verificationLogin = function()
    {
        let element_parent = $("#lien_connexion");
        let login = $(this).val();

        $.ajax(
        {
            url: element_parent.attr("verification-login-url"),
            type: 'get',
            data: {'login': login},
            dataType: 'json',
            success: function (data)
            {
                if (!data.login_existe)
                {
                    // il reste à mettre le contour du champ en rouge
                    alert("Cet utilisateur n'existe pas. Veuillez vérifier votre saisie.");
                }
                else
                {
                    $("#modal-authentification .modal-content").html(data.html_form);
                }
            }
        });
    };

    /* Liens */
    /* ----- */

    $("#lien_connexion").click(chargementFormulaireAuthentification);
    $("#modal-authentification").on("submit", ".js-authentification-creation-formulaire", sauvegardeFormulaireAuthentification);
    $("#modal-authentification").on("change", "#id_login", verificationLogin);
});
