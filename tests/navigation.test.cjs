"use strict";

const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");
const vm = require("node:vm");

function createNavigationHarness() {
  const documentListeners = {};
  const buttonListeners = {};
  const navigationListeners = {};
  const documentClasses = new Set();
  const attributes = { "aria-expanded": "false" };
  const classes = new Set();
  const label = { textContent: "Open navigation" };
  let focusCount = 0;

  const menuButton = {
    addEventListener: (name, callback) => { buttonListeners[name] = callback; },
    getAttribute: (name) => attributes[name] ?? null,
    setAttribute: (name, value) => { attributes[name] = value; },
    querySelector: () => label,
    focus: () => { focusCount += 1; },
  };
  const link = {
    addEventListener: (name, callback) => { navigationListeners[name] = callback; },
  };
  const navigation = {
    classList: {
      add: (name) => classes.add(name),
      remove: (name) => classes.delete(name),
    },
    querySelectorAll: () => [link],
  };
  const document = {
    addEventListener: (name, callback) => { documentListeners[name] = callback; },
    documentElement: { classList: { add: (name) => documentClasses.add(name) } },
    getElementById: (id) => ({
      "menu-toggle": menuButton,
      "primary-nav": navigation,
    })[id] ?? null,
  };

  const source = fs.readFileSync(
    path.join(__dirname, "..", "src", "js", "site.js"),
    "utf8"
  );
  vm.runInNewContext(source, { document });
  documentListeners.DOMContentLoaded();

  return {
    attributes,
    classes,
    documentClasses,
    label,
    buttonListeners,
    navigationListeners,
    documentListeners,
    get focusCount() { return focusCount; },
  };
}

test("mobile navigation updates expanded state and its screen-reader label", () => {
  const h = createNavigationHarness();
  h.buttonListeners.click();
  assert.equal(h.attributes["aria-expanded"], "true");
  assert.equal(h.label.textContent, "Close navigation");
  assert.equal(h.classes.has("is-open"), true);
  assert.equal(h.documentClasses.has("has-js"), true);

  h.buttonListeners.click();
  assert.equal(h.attributes["aria-expanded"], "false");
  assert.equal(h.label.textContent, "Open navigation");
  assert.equal(h.classes.has("is-open"), false);
});

test("Escape closes navigation and restores focus to the menu toggle", () => {
  const h = createNavigationHarness();
  h.buttonListeners.click();
  h.documentListeners.keydown({ key: "Escape" });
  assert.equal(h.attributes["aria-expanded"], "false");
  assert.equal(h.label.textContent, "Open navigation");
  assert.equal(h.classes.has("is-open"), false);
  assert.equal(h.focusCount, 1);
});

test("activating a navigation link closes the menu without stealing focus", () => {
  const h = createNavigationHarness();
  h.buttonListeners.click();
  h.navigationListeners.click();
  assert.equal(h.attributes["aria-expanded"], "false");
  assert.equal(h.label.textContent, "Open navigation");
  assert.equal(h.classes.has("is-open"), false);
  assert.equal(h.focusCount, 0);
});
