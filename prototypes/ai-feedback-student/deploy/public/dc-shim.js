/* Tiny stand-in for the Design Component runtime, so the same artboards run as
   plain web pages on the prototype server. It supports only what these screens
   use: {{holes}} in text and attributes, <sc-if value="{{flag}}">, event
   attributes bound to functions from renderVals(), defaultValue on inputs, and
   state / setState / componentDidMount / componentDidUpdate.

   Generated pages hold the artboard markup in <template id="dc-template">,
   render into <div id="dc-root">, and call __dcBoot(Component) at the end. */
(function () {
  "use strict";

  var HOLE = /\{\{\s*([A-Za-z_$][\w.$]*)\s*\}\}/g;
  var WHOLE = /^\{\{\s*([A-Za-z_$][\w.$]*)\s*\}\}$/;

  function lookup(vals, path) {
    return path.split(".").reduce(function (o, k) {
      return o === null || o === undefined ? undefined : o[k];
    }, vals);
  }

  function interp(text, vals) {
    return text.replace(HOLE, function (_m, path) {
      var v = lookup(vals, path);
      return v === null || v === undefined || typeof v === "function" ? "" : String(v);
    });
  }

  function DCLogic(props) {
    this.props = props || {};
    this.state = {};
  }
  DCLogic.prototype.setState = function (patch) {
    var prev = Object.assign({}, this.state);
    var next = typeof patch === "function" ? patch(this.state) : patch;
    this.state = Object.assign({}, this.state, next);
    this._render();
    if (typeof this.componentDidUpdate === "function") this.componentDidUpdate(this.props, prev);
  };
  DCLogic.prototype.forceUpdate = function () {
    this._render();
  };
  DCLogic.prototype.renderVals = function () {
    return {};
  };
  window.DCLogic = DCLogic;

  /* Clone the template into live nodes, resolving holes, branches and handlers. */
  function build(src, dest, vals) {
    var nodes = src.childNodes;
    for (var i = 0; i < nodes.length; i++) {
      var node = nodes[i];
      if (node.nodeType === 3) {
        dest.appendChild(document.createTextNode(interp(node.nodeValue, vals)));
        continue;
      }
      if (node.nodeType !== 1) continue;

      if (node.tagName.toLowerCase() === "sc-if") {
        var cond = (node.getAttribute("value") || "").match(WHOLE);
        if (cond && lookup(vals, cond[1])) build(node, dest, vals);
        continue;
      }

      /* localName, not tagName: createElementNS is case-sensitive, and an
         uppercase name in the HTML namespace yields an inert unknown element
         (no href on a link, no value on a textarea). */
      var el = document.createElementNS(node.namespaceURI, node.localName);
      var attrs = node.attributes;
      for (var a = 0; a < attrs.length; a++) {
        var name = attrs[a].name;
        var raw = attrs[a].value;
        var whole = raw.match(WHOLE);

        if (name.length > 2 && name.slice(0, 2) === "on") {
          var fn = whole ? lookup(vals, whole[1]) : null;
          if (typeof fn === "function") el.addEventListener(name.slice(2).toLowerCase(), fn);
          continue;
        }
        if (name === "defaultvalue") {
          el.value = whole ? lookup(vals, whole[1]) || "" : raw;
          continue;
        }
        el.setAttribute(name, interp(raw, vals));
      }
      build(node, el, vals);
      dest.appendChild(el);
    }
  }

  /* A re-render replaces the tree, so carry the caret across it. */
  function render(root, template, inst) {
    var vals = inst.renderVals() || {};
    var active = document.activeElement;
    var keepId = active && active.id ? active.id : null;
    var caret = active && typeof active.selectionStart === "number" ? active.selectionStart : null;

    var frag = document.createDocumentFragment();
    build(template, frag, vals);
    root.textContent = "";
    root.appendChild(frag);

    if (keepId) {
      var again = document.getElementById(keepId);
      if (again && typeof again.focus === "function") {
        again.focus({ preventScroll: true });
        if (caret !== null && typeof again.setSelectionRange === "function") {
          try {
            again.setSelectionRange(caret, caret);
          } catch (e) {
            /* an input that does not take a selection */
          }
        }
      }
    }
  }

  window.__dcBoot = function (Component) {
    var template = document.getElementById("dc-template").content;
    var root = document.getElementById("dc-root");
    var inst = new Component({});
    if (!inst.state) inst.state = {};
    inst._render = function () {
      render(root, template, inst);
    };
    inst._render();
    if (typeof inst.componentDidMount === "function") inst.componentDidMount();
    window.__dc = inst;
  };
})();
