/**
 * Client-side scripts for webview
 */

import { generateStateScript } from './state';
import { generateVirtualListScript } from './virtualList';

export function generateWebviewScript(totalAccounts: number): string {
  return `
    const vscode = acquireVsCodeApi();
    let pendingAction = null;
    
    ${generateStateScript()}
    ${generateVirtualListScript()}
    
    // UI Actions
    function toggleCompact() {
      document.body.classList.toggle('compact');
      setState({ compact: document.body.classList.contains('compact') });
      vscode.postMessage({ command: 'toggleCompact' });
    }
    
    function openSettings() {
      const panel = document.getElementById('settingsPanel');
      panel.classList.toggle('visible');
      setState({ settingsOpen: panel.classList.contains('visible') });
    }
    
    function toggleAutoSwitch(enabled) {
      vscode.postMessage({ command: 'toggleAutoSwitch', enabled });
    }
    
    function updateSetting(key, value) {
      vscode.postMessage({ command: 'updateSetting', key, value });
    }
    
    function changeLanguage(lang) {
      vscode.postMessage({ command: 'setLanguage', language: lang });
    }
    
    function startAutoReg() {
      console.log('startAutoReg clicked');
      vscode.postMessage({ command: 'startAutoReg' });
    }
    
    function importToken() {
      vscode.postMessage({ command: 'importToken' });
    }
    
    function refresh() {
      vscode.postMessage({ command: 'refresh' });
    }
    
    function exportAccounts() {
      vscode.postMessage({ command: 'exportAccounts' });
    }
    
    function switchAccount(filename) {
      vscode.postMessage({ command: 'switchAccount', email: filename });
    }
    
    function openUpdateUrl(url) {
      vscode.postMessage({ command: 'openUrl', url: url });
    }
    
    function copyToken(filename) {
      vscode.postMessage({ command: 'copyToken', email: filename });
    }
    
    function viewQuota(filename) {
      vscode.postMessage({ command: 'viewQuota', email: filename });
    }
    
    function refreshToken(filename) {
      vscode.postMessage({ command: 'refreshToken', email: filename });
    }
    
    function clearConsole() {
      vscode.postMessage({ command: 'clearConsole' });
    }
    
    // Dialog
    function confirmDeleteExpired() {
      pendingAction = { type: 'deleteExpired' };
      const lang = document.body.dataset.lang || 'en';
      const titles = { 
        en: 'Delete Expired Accounts', ru: 'Удалить истёкшие', zh: '删除过期账户',
        es: 'Eliminar expiradas', pt: 'Excluir expiradas', ja: '期限切れを削除',
        de: 'Abgelaufene löschen', fr: 'Supprimer expirés', ko: '만료된 계정 삭제', hi: 'समाप्त हटाएं'
      };
      const texts = { 
        en: 'Delete all expired accounts? This cannot be undone.',
        ru: 'Удалить все истёкшие аккаунты? Это нельзя отменить.',
        zh: '删除所有过期账户？此操作无法撤销。',
        es: '¿Eliminar todas las cuentas expiradas? No se puede deshacer.',
        pt: 'Excluir todas as contas expiradas? Não pode ser desfeito.',
        ja: '期限切れのアカウントをすべて削除しますか？元に戻せません。',
        de: 'Alle abgelaufenen Konten löschen? Kann nicht rückgängig gemacht werden.',
        fr: 'Supprimer tous les comptes expirés ? Irréversible.',
        ko: '만료된 모든 계정을 삭제하시겠습니까? 되돌릴 수 없습니다.',
        hi: 'सभी समाप्त खाते हटाएं? यह पूर्ववत नहीं किया जा सकता।'
      };
      document.getElementById('dialogTitle').textContent = titles[lang] || titles.en;
      document.getElementById('dialogText').textContent = texts[lang] || texts.en;
      document.getElementById('dialogOverlay').classList.add('visible');
    }
    
    function confirmDelete(filename) {
      pendingAction = { type: 'delete', filename };
      const lang = document.body.dataset.lang || 'en';
      const titles = { 
        en: 'Delete Account', ru: 'Удалить аккаунт', zh: '删除账户', 
        es: 'Eliminar cuenta', pt: 'Excluir conta', ja: 'アカウントを削除',
        de: 'Konto löschen', fr: 'Supprimer le compte', ko: '계정 삭제', hi: 'खाता हटाएं'
      };
      const texts = { 
        en: 'Are you sure you want to delete this account?', 
        ru: 'Вы уверены, что хотите удалить этот аккаунт?',
        zh: '您确定要删除此账户吗？', es: '¿Está seguro de que desea eliminar esta cuenta?',
        pt: 'Tem certeza de que deseja excluir esta conta?', ja: 'このアカウントを削除してもよろしいですか？',
        de: 'Sind Sie sicher, dass Sie dieses Konto löschen möchten?', 
        fr: 'Êtes-vous sûr de vouloir supprimer ce compte ?',
        ko: '이 계정을 삭제하시겠습니까?', hi: 'क्या आप वाकई इस खाते को हटाना चाहते हैं?'
      };
      document.getElementById('dialogTitle').textContent = titles[lang] || titles.en;
      document.getElementById('dialogText').textContent = texts[lang] || texts.en;
      document.getElementById('dialogOverlay').classList.add('visible');
    }
    
    function closeDialog() {
      document.getElementById('dialogOverlay').classList.remove('visible');
      pendingAction = null;
    }
    
    function dialogAction() {
      if (pendingAction?.type === 'delete') {
        vscode.postMessage({ command: 'deleteAccount', email: pendingAction.filename });
      }
      closeDialog();
    }
    
    // Filtering & Sorting
    function filterAccounts(filter) {
      setState({ filter });
      document.querySelectorAll('.filter-tab').forEach(tab => {
        tab.classList.toggle('active', tab.textContent.toLowerCase() === filter);
      });
      applyFilters();
    }
    
    function toggleHideExpired(hide) {
      setState({ hideExpired: hide });
      vscode.postMessage({ command: 'setHideExpired', hide });
      applyFilters();
    }
    
    function applyFilters() {
      const state = getState();
      const filter = state.filter || 'all';
      const hideExpired = state.hideExpired || false;
      
      document.querySelectorAll('.card').forEach(card => {
        const isExpired = card.classList.contains('expired');
        let show = true;
        
        // Apply tab filter
        if (filter === 'valid' && isExpired) show = false;
        if (filter === 'expired' && !isExpired) show = false;
        
        // Apply hide expired checkbox
        if (hideExpired && isExpired) show = false;
        
        card.style.display = show ? '' : 'none';
      });
    }
    
    function sortAccounts(sort) {
      setState({ sort });
      vscode.postMessage({ command: 'sortAccounts', sort });
    }
    
    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        closeDialog();
        document.getElementById('settingsPanel')?.classList.remove('visible');
      }
      if (e.ctrlKey || e.metaKey) {
        if (e.key === 'r') { e.preventDefault(); refresh(); }
        if (e.key === 'n') { e.preventDefault(); startAutoReg(); }
        if (e.key === 'f') { e.preventDefault(); document.getElementById('searchInput')?.focus(); }
      }
    });
    
    // Initialize
    document.addEventListener('DOMContentLoaded', () => {
      // Restore state
      const state = getState();
      if (state.compact) document.body.classList.add('compact');
      if (state.settingsOpen) document.getElementById('settingsPanel')?.classList.add('visible');
      if (state.filter && state.filter !== 'all') filterAccounts(state.filter);
      
      // Sync hideExpired checkbox with initial state from server
      const checkbox = document.getElementById('hideExpiredCheckbox');
      if (checkbox && checkbox.checked) {
        setState({ hideExpired: true });
        applyFilters();
      }
      
      // Auto-scroll console
      const consoleBody = document.getElementById('consoleBody');
      if (consoleBody) consoleBody.scrollTop = consoleBody.scrollHeight;
      
      // Init virtual list if needed
      initVirtualList(${totalAccounts});
    });
  `;
}
