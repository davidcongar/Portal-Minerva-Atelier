function openSqlModal() {
    document.getElementById('sqlModalBackdrop')?.classList.remove('hidden');
    document.getElementById('sqlModal')?.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}
function closeSqlModal() {
    document.getElementById('sqlModalBackdrop')?.classList.add('hidden');
    document.getElementById('sqlModal')?.classList.add('hidden');
    document.body.style.overflow = '';
}
function copySqlToClipboard() {
    if (!sqlText) return;
    navigator.clipboard.writeText(sqlText);
}
document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeSqlModal();
});