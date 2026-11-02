// Espaces insécables avant ? ! : ; » et après « (règle française), dans tout le texte de la page,
// pour que la ponctuation ne se retrouve jamais seule en début de ligne.
window.typo = (root = document.body) => {
  const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, { acceptNode: n => n.parentElement.closest("script,style") ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT });
  for (let n; (n = w.nextNode());) {
    const v = n.nodeValue.replace(/ ([?!:;»])/g, " $1").replace(/« /g, "« ").replace(/(\d) (\d{3})\b/g, "$1 $2");
    if (v !== n.nodeValue) n.nodeValue = v;
  }
};
