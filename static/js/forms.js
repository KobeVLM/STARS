document.addEventListener('DOMContentLoaded', () => {
    initUploadPreview();
    initAvatarPreview();
});

/**
 * Initialize image preview for artwork upload
 */
function initUploadPreview() {
    const imageInput = document.getElementById('id_image');
    const imagePreview = document.getElementById('imagePreview');
    const previewImg = document.getElementById('previewImg');
    const uploadArea = document.getElementById('uploadArea');
    const removeBtn = document.querySelector('#imagePreview button');

    if (!imageInput || !imagePreview || !previewImg || !uploadArea) return;

    imageInput.addEventListener('change', function (e) {
        const file = e.target.files[0];

        if (file) {
            const reader = new FileReader();

            reader.onload = function (e) {
                previewImg.src = e.target.result;
                imagePreview.style.display = 'block';
                uploadArea.style.borderColor = 'var(--primary)';
            };

            reader.readAsDataURL(file);
        }
    });

    if (removeBtn) {
        removeBtn.addEventListener('click', function () {
            imageInput.value = '';
            imagePreview.style.display = 'none';
            uploadArea.style.borderColor = 'rgba(112, 132, 217, 0.5)'; // Reset to default border color
        });
    }
}

/**
 * Initialize avatar preview for profile edit
 */
function initAvatarPreview() {
    const avatarInput = document.getElementById('id_avatar');
    const avatarPreview = document.getElementById('avatarPreview');
    const removeBtn = document.querySelector('.form-group button[onclick="clearAvatar()"]'); // Selecting by onclick attribute for now, ideally should use ID or class

    if (!avatarInput || !avatarPreview) return;

    // Get default avatar URL from data attribute
    const defaultAvatar = avatarPreview.dataset.defaultSrc;

    avatarInput.addEventListener('change', function (e) {
        const file = e.target.files[0];

        if (file) {
            const reader = new FileReader();

            reader.onload = function (e) {
                avatarPreview.src = e.target.result;
            };

            reader.readAsDataURL(file);
        }
    });

    // Replace the inline onclick handler with event listener if button exists
    if (removeBtn) {
        removeBtn.removeAttribute('onclick'); // Remove inline handler
        removeBtn.addEventListener('click', function () {
            avatarInput.value = '';
            if (defaultAvatar) {
                avatarPreview.src = defaultAvatar;
            }
        });
    }
}
