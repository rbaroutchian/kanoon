// تابع بررسی وضعیت ورود کاربر (ساده و شبیه‌سازی شده)
function checkLogin() {
    // در نسخه واقعی این اطلاعات از سرور یا کوکی خوانده می‌شود
    const isLoggedIn = localStorage.getItem('user_logged_in');
    return isLoggedIn === 'true';
}

// 1. منطق پیش‌ثبت‌نام کلاس‌ها
function preRegister(className) {
    if (!checkLogin()) {
        alert("لطفا ابتدا وارد حساب کاربری خود شوید یا ثبت نام کنید.");
        window.location.href = "login.html";
        return;
    }

    // شبیه‌سازی ارسال به دیتابیس
    const confirmMsg = confirm(`آیا مایل به پیش‌ثبت‌نام در کلاس "${className}" هستید؟\nبا شما تماس گرفته خواهد شد.`);
    if (confirmMsg) {
        alert("درخواست شما با موفقیت ثبت شد. همکاران ما به زودی با شما تماس می‌گیرند.");
        // اینجا در واقعیت باید یک درخواست API به بک‌اند (Python/Node/PHP) ارسال شود
    }
}

// 2. منطق رزرو بلیط سینما و تولید کد رهگیری
function reserveTicket(event) {
    event.preventDefault(); // جلوگیری از رفرش شدن صفحه

    if (!checkLogin()) {
        alert("برای رزرو بلیط ابتدا باید وارد شوید.");
        window.location.href = "login.html";
        return;
    }

    const movie = document.getElementById('movieSelect').value;
    const sans = document.getElementById('sansSelect').value;
    const count = document.getElementById('ticketCount').value;

    // تولید یک کد رهگیری تصادفی 6 رقمی
    const trackingCode = Math.floor(100000 + Math.random() * 900000);

    // نمایش نتیجه
    document.getElementById('resMovie').innerText = `${movie} - ساعت ${sans} (${count} نفر)`;
    document.getElementById('trackingCode').innerText = trackingCode;

    // نمایش باکس نتیجه
    document.getElementById('ticketResult').classList.remove('d-none');
    document.getElementById('cinemaForm').style.display = 'none';
}

// 3. منطق ساده ورود (Login)
function handleLogin(event) {
    event.preventDefault();
    const phone = document.getElementById('phoneInput').value;

    if (phone.length >= 10) {
        localStorage.setItem('user_logged_in', 'true');
        alert("ورود با موفقیت انجام شد.");
        window.location.href = "index.html";
    } else {
        alert("لطفا شماره موبایل معتبر وارد کنید.");
    }
}


