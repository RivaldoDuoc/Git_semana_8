$(document).ready(function() {
    // Función para limpiar mensajes de error
    function limpiarMensajesError() {
        $('#nombre-error').text('');
        $('#appaterno-error').text('');
        $('#apmaterno-error').text('');
        $('#email-error').text('');
        $('#nomusuario-error').text('');
        $('#fecha-error').text('');
        $('#password-error').text('');
        $('#password2-error').text('');
    }

    // Validaciones y manejo del envío del formulario de registro
    $('#formulario-registro').submit(function(event) {
        event.preventDefault(); // Evita el envío inmediato del formulario

        // Limpiar mensajes de error antes de validar
        limpiarMensajesError();

        // Captura de valores
        const nombre = $('#nombre').val().trim();
        const appaterno = $('#appaterno').val().trim();
        const apmaterno = $('#apmaterno').val().trim();
        const email = $('#email').val().trim();
        const username = $('#nomusuario').val().trim();
        const password1 = $('#password').val().trim();
        const password2 = $('#password2').val().trim();
        const fechaValue = $('#fecha').val();

        // Validaciones
        if (!nombre) {
            $('#nombre-error').text('El campo Nombre no puede estar vacío.');
            return;
        }
        if (!appaterno) {
            $('#appaterno-error').text('El campo Apellido Paterno no puede estar vacío.');
            return;
        }
        if (!apmaterno) {
            $('#apmaterno-error').text('El campo Apellido Materno no puede estar vacío.');
            return;
        }
        if (!email) {
            $('#email-error').text('El campo Correo Electrónico no puede estar vacío.');
            return;
        }
        if (!username) {
            $('#nomusuario-error').text('El campo Nombre de Usuario no puede estar vacío.');
            return;
        }
        if (!password1) {
            $('#password-error').text('El campo Contraseña no puede estar vacío.');
            return;
        }
        if (password1 !== password2) {
            $('#password-error').text('Las contraseñas no coinciden.');
            return;
        }
        if (password1.length < 8) {
            $('#password-error').text('La contraseña debe tener al menos 8 caracteres.');
            return;
        }
        if (!/\d/.test(password1)) {
            $('#password-error').text('La contraseña debe contener al menos un número.');
            return;
        }
        // Validación de edad
        if (!fechaValue) {
            $('#fecha-error').text('Debe ingresar una fecha válida');
            return;
        }

        const fecha = new Date(fechaValue);
        const hoy = new Date();
        let edad = hoy.getFullYear() - fecha.getFullYear();
        const mes = hoy.getMonth() - fecha.getMonth();
        if (mes < 0 || (mes === 0 && hoy.getDate() < fecha.getDate())) {
            edad--;
        }
        if (edad < 13) {
            $('#fecha-error').text('Solo pueden registrarse mayores de 13 años');
            return;
        }

        // Envío de formulario
        this.submit(); // Se envía el formulario si todas las validaciones están bien
    });

    // Función para limpiar campos
    window.limpiarCampos = function() {
        console.log("Limpiar campos ejecutándose");
        $('#formulario-registro')[0].reset(); // Restablece el formulario
        limpiarMensajesError(); // Limpia los mensajes de error
    };

    // Manejo del envío del formulario de inicio de sesión
    $('#formulario-login').submit(function(event) {
        event.preventDefault(); // Evita el envío del formulario
        
        // Obtener los valores
        var nombreUsuario = $('#username').val().trim();
        var contraseña = $('#passwordLogin').val().trim();
        
        // Limpiar mensajes de error
        $('#username-error').text('');
        $('#password-error-login').text('');

        if (nombreUsuario === '' && contraseña === '') {
            $('#username-error').text('Por favor ingresa tu nombre de usuario.');
            $('#password-error-login').text('Falta la contraseña.');
        } else if (nombreUsuario === '') {
            $('#username-error').text('Debe ingresar un nombre de usuario o e-mail');
        } else if (contraseña === '') {
            $('#password-error-login').text('Debe ingresar una contraseña.');
        } else {
            $('#username-error').text('Credenciales ingresadas con éxito.');
            this.submit(); // Envío si los datos son válidos
        }
    });

    // Función para agregar al carrito
    window.agregarAlCarrito = function(event) {
        $('.carrito-mensaje').hide(); // Oculta cualquier mensaje
        $(event.target).siblings('.carrito-mensaje').show(); // Muestra mensaje específico
    };

    $('#recovery-form').on('submit', function(e) {
        e.preventDefault(); // Evita el envío del formulario por defecto

        var email = $('#email').val();
        if (email) {
            $('#success-message').show();
            $('#button-error-message').hide();
        } else {
            $('#button-error-message').text('Por favor, introduce un correo válido.').show();
            $('#success-message').hide();
        }
    });
});
