[1mdiff --git a/.gitignore b/.gitignore[m
[1mnew file mode 100644[m
[1mindex 0000000..99801e6[m
[1m--- /dev/null[m
[1m+++ b/.gitignore[m
[36m@@ -0,0 +1,100 @@[m
[32m+[m[32m# Python[m
[32m+[m[32m*.py[cod][m
[32m+[m[32m*$py.class[m
[32m+[m[32m__pycache__/[m
[32m+[m[32m*.so[m
[32m+[m[32m*.egg[m
[32m+[m[32m*.egg-info/[m
[32m+[m[32mdist/[m
[32m+[m[32mbuild/[m
[32m+[m[32meggs/[m
[32m+[m[32m.eggs/[m
[32m+[m[32mlib/[m
[32m+[m[32mlib64/[m
[32m+[m[32mparts/[m
[32m+[m[32msdist/[m
[32m+[m[32mvar/[m
[32m+[m[32mwheels/[m
[32m+[m[32m*.whl[m
[32m+[m[32m.Python[m
[32m+[m
[32m+[m[32m# Django[m
[32m+[m[32m*.log[m
[32m+[m[32mlocal_settings.py[m
[32m+[m[32mdb.sqlite3[m
[32m+[m[32mdb.sqlite3-journal[m
[32m+[m[32m/media[m
[32m+[m[32m/staticfiles[m
[32m+[m[32m/static[m
[32m+[m
[32m+[m[32m# Environment variables[m
[32m+[m[32m.env[m
[32m+[m[32m.env.local[m
[32m+[m[32m.env.*.local[m
[32m+[m[32m*.env[m
[32m+[m
[32m+[m[32m# Virtual environments[m
[32m+[m[32mvenv/[m
[32m+[m[32mENV/[m
[32m+[m[32menv/[m
[32m+[m[32m.venv[m
[32m+[m
[32m+[m[32m# IDE - VSCode[m
[32m+[m[32m.vscode/[m
[32m+[m[32m*.code-workspace[m
[32m+[m
[32m+[m[32m# IDE - PyCharm[m
[32m+[m[32m.idea/[m
[32m+[m[32m*.iml[m
[32m+[m[32m*.iws[m
[32m+[m[32m.idea_modules/[m
[32m+[m
[32m+[m[32m# IDEs - Other[m
[32m+[m[32m*.swp[m
[32m+[m[32m*.swo[m
[32m+[m[32m*~[m
[32m+[m[32m.project[m
[32m+[m[32m.pydevproject[m
[32m+[m[32m.settings/[m
[32m+[m
[32m+[m[32m# OS[m
[32m+[m[32m.DS_Store[m
[32m+[m[32m.DS_Store?[m
[32m+[m[32m._*[m
[32m+[m[32m.Spotlight-V100[m
[32m+[m[32m.Trashes[m
[32m+[m[32mehthumbs.db[m
[32m+[m[32mThumbs.db[m
[32m+[m[32mDesktop.ini[m
[32m+[m
[32m+[m[32m# Testing[m
[32m+[m[32m.coverage[m
[32m+[m[32m.pytest_cache/[m
[32m+[m[32mhtmlcov/[m
[32m+[m[32m.tox/[m
[32m+[m[32m.nox/[m
[32m+[m
[32m+[m[32m# Migrations (optional - uncomment if you want to ignore migrations)[m
[32m+[m[32m# */migrations/*.py[m
[32m+[m[32m# !*/migrations/__init__.py[m
[32m+[m
[32m+[m[32m# Jupyter Notebook[m
[32m+[m[32m.ipynb_checkpoints[m
[32m+[m
[32m+[m[32m# Node (if using any frontend tools)[m
[32m+[m[32mnode_modules/[m
[32m+[m[32mnpm-debug.log*[m
[32m+[m[32myarn-debug.log*[m
[32m+[m[32myarn-error.log*[m
[32m+[m
[32m+[m[32m# Backup files[m
[32m+[m[32m*.bak[m
[32m+[m[32m*.swp[m
[32m+[m[32m*.tmp[m
[32m+[m[32m*~[m
[32m+[m
[32m+[m[32m# Collected static files[m
[32m+[m[32m/static_collected/[m
[32m+[m
[32m+[m[32m#database[m
[32m+[m[32mdb.sqlite3[m
\ No newline at end of file[m
[1mdiff --git a/db.sqlite3 b/db.sqlite3[m
[1mindex 5eced97..b5bdd8f 100644[m
Binary files a/db.sqlite3 and b/db.sqlite3 differ
[1mdiff --git a/media/artworks/Media_27.jpg b/media/artworks/Media_27.jpg[m
[1mdeleted file mode 100644[m
[1mindex 8bd111c..0000000[m
Binary files a/media/artworks/Media_27.jpg and /dev/null differ
[1mdiff --git a/media/artworks/Untitled.png b/media/artworks/Untitled.png[m
[1mdeleted file mode 100644[m
[1mindex ad0aa93..0000000[m
Binary files a/media/artworks/Untitled.png and /dev/null differ
[1mdiff --git a/media/artworks/images.jfif b/media/artworks/images.jfif[m
[1mnew file mode 100644[m
[1mindex 0000000..4a74f7e[m
Binary files /dev/null and b/media/artworks/images.jfif differ
[1mdiff --git a/media/artworks/pngimg.com_-_squid_game_PNG64.png b/media/artworks/pngimg.com_-_squid_game_PNG64.png[m
[1mdeleted file mode 100644[m
[1mindex 2f2781f..0000000[m
Binary files a/media/artworks/pngimg.com_-_squid_game_PNG64.png and /dev/null differ
[1mdiff --git a/media/avatars/images.jfif b/media/avatars/images.jfif[m
[1mnew file mode 100644[m
[1mindex 0000000..4a74f7e[m
Binary files /dev/null and b/media/avatars/images.jfif differ
[1mdiff --git a/static/css/auth.css b/static/css/auth.css[m
[1mnew file mode 100644[m
[1mindex 0000000..bec15ab[m
[1m--- /dev/null[m
[1m+++ b/static/css/auth.css[m
[36m@@ -0,0 +1,46 @@[m
[32m+[m[32m/* Auth Pages Styles */[m
[32m+[m[32m.auth-container {[m
[32m+[m[32m    max-width: 500px;[m
[32m+[m[32m    margin: 60px auto;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m.auth-card {[m
[32m+[m[32m    padding: 40px;[m
[32m+[m[32m    background-color: white;[m
[32m+[m[32m    border: 1px solid rgba(112, 132, 217, 0.2);[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m.auth-title {[m
[32m+[m[32m    text-align: center;[m
[32m+[m[32m    margin-bottom: 30px;[m
[32m+[m[32m    color: var(--primary-dark);[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m.auth-footer {[m
[32m+[m[32m    text-align: center;[m
[32m+[m[32m    margin-top: 20px;[m
[32m+[m[32m    color: var(--text-muted);[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m.auth-link {[m
[32m+[m[32m    color: var(--primary);[m
[32m+[m[32m    text-decoration: none;[m
[32m+[m[32m    font-weight: 600;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m.auth-link:hover {[m
[32m+[m[32m    text-decoration: underline;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m.error-message {[m
[32m+[m[32m    color: #d63031;[m
[32m+[m[32m    margin-bottom: 15px;[m
[32m+[m[32m    font-size: 0.9rem;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m.field-error {[m
[32m+[m[32m    color: #d63031;[m
[32m+[m[32m    font-size: 0.85rem;[m
[32m+[m[32m    margin-top: 5px;[m
[32m+[m[32m    display: block;[m
[32m+[m[32m}[m
\ No newline at end of file[m
[1mdiff --git a/static/css/base.css b/static/css/base.css[m
[1mnew file mode 100644[m
[1mindex 0000000..d3be1fc[m
[1m--- /dev/null[m
[1m+++ b/static/css/base.css[m
[36m@@ -0,0 +1,77 @@[m
[32m+[m[32m* {[m
[32m+[m[32m    margin: 0;[m
[32m+[m[32m    padding: 0;[m
[32m+[m[32m    box-sizing: border-box;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32mbody {[m
[32m+[m[32m    font-family: 'Poppins', sans-serif;[m
[32m+[m[32m    background: var(--bg-color);[m
[32m+[m[32m    color: var(--text-dark);[m
[32m+[m[32m    line-height: 1.6;[m
[32m+[m[32m    min-height: 100vh;[m
[32m+[m[32m    position: relative;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m/* --- Starfield Background --- */[m
[32m+[m[32mbody::before {[m
[32m+[m[32m    content: '';[m
[32m+[m[32m    position: fixed;[m
[32m+[m[32m    top: 0;[m
[32m+[m[32m    left: 0;[m
[32m+[m[32m    width: 100%;[m
[32m+[m[32m    height: 100%;[m
[32m+[m[32m    background-image:[m
[32m+[m[32m        radial-gradient(2px 2px at 20px 30px, #F5F1AD, transparent),[m
[32m+[m[32m        radial-gradient(2px 2px at 40px 70px, #D8CE73, transparent),[m
[32m+[m[32m        radial-gradient(1px 1px at 90px 40px, white, transparent),[m
[32m+[m[32m        radial-gradient(2px 2px at 160px 120px, #F5F1AD, transparent),[m
[32m+[m[32m        radial-gradient(1px 1px at 230px 80px, #D8CE73, transparent),[m
[32m+[m[32m        radial-gradient(2px 2px at 300px 150px, white, transparent),[m
[32m+[m[32m        radial-gradient(1px 1px at 370px 60px, #F5F1AD, transparent),[m
[32m+[m[32m        radial-gradient(2px 2px at 450px 200px, #D8CE73, transparent);[m
[32m+[m[32m    background-size: 500px 250px;[m
[32m+[m[32m    animation: twinkle 8s ease-in-out infinite;[m
[32m+[m[32m    pointer-events: none;[m
[32m+[m[32m    z-index: -1;[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m@keyframes twinkle {[m
[32m+[m
[32m+[m[32m    0%,[m
[32m+[m[32m    100% {[m
[32m+[m[32m        opacity: 0.7;[m
[32m+[m[32m    }[m
[32m+[m
[32m+[m[32m    50% {[m
[32m+[m[32m        opacity: 1;[m
[32m+[m[32m    }[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32m@keyframes pulse {[m
[32m+[m
[32m+[m[32m    0%,[m
[32m+[m[32m    100% {[m
[32m+[m[32m        opacity: 1;[m
[32m+[m[32m    }[m
[32m+[m
[32m+[m[32m    50% {[m
[32m+[m[32m        opacity: 0.85;[m
[32m+[m[32m    }[m
[32m+[m[32m}[m
[32m+[m
[32m+[m