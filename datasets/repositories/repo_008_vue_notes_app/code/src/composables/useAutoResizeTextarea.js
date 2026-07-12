export function resizeToFit(el) {
  if (!el) return;
  el.style.height = "auto";
  el.style.height = `${el.scrollHeight}px`;
}

export function useAutoResizeTextarea() {
  function onInput(event) {
    resizeToFit(event.target);
  }
  return { onInput };
}
