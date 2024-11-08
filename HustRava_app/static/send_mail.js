$(document).ready(function() {
    $('#send_captcha').click(function(e) {
        e.preventDefault();
        const email = $('#user_email').val();
        const csrfToken = $('#csrf_token').val();  // 从隐藏字段获取 CSRF Token
        if (!email) {
            alert('请填写邮箱');
            return;
        }

        $.ajax({
            url: sendCaptchaUrl,  // 使用全局变量 sendCaptchaUrl
            type: 'POST',
            data: {
                'user_email': email,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function(response) {
                if (response.message) {
                    alert(response.message);
                } else if (response.error) {
                    alert(response.error);
                }
            },
            error: function(xhr, status, error) {
                // 处理 AJAX 请求失败的情况
                if (xhr.status === 400) {
                    // 如果是 400 错误，可能是因为表单验证失败
                    alert('验证码发送失败，请检查邮箱格式或重试');
                } else {
                    // 其他错误
                    alert('验证码发送失败，请重试');
                }
            }
        });
    });
});