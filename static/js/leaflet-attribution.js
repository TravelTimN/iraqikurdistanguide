/* jshint esversion: 11 */

L.Control.CondensedAttribution = L.Control.Attribution.extend({
    options: {
        emblem: "<span class='fw-bold'>?</span>",
    },
    onAdd: function (map) {
        let vMaj = parseInt(L.version.split(".")[0]);
        if (vMaj >= 1) {
            map.attributionControl = this;
        }

        this._container = L.DomUtil.create("div", "leaflet-control-attribution");
        if (L.DomEvent) {
            L.DomEvent.disableClickPropagation(this._container);
        }

        for (let i in map._layers) {
            if (map._layers[i].getAttribution) {
                this.addAttribution(map._layers[i].getAttribution());
            }
        }

        // attribution properly supplied per map, but 'map' and 'this' do not recognize any layers.
        // let i = 0;
        // map.eachLayer(function() {i += 1;});
        // console.log(`Map has ${i} layers.`); // result: 0 layers

        if (vMaj < 1) {
            map
                .on("layeradd", this._onLayerAdd, this)
                .on("layerremove", this._onLayerRemove, this);
        }

        this._update();

        L.DomUtil.addClass(this._container, "leaflet-condensed-attribution");

        return this._container;
    },
    _update: function () {
        if (!this._map) {
            return;
        }

        let attribs = [];

        for (let i in this._attributions) {
            if (this._attributions[i]) {
                attribs.push(i);
            }
        }

        let prefixAndAttribs = [];

        if (this.options.prefix) {
            prefixAndAttribs.push(this.options.prefix);
        }
        if (attribs.length) {
            prefixAndAttribs.push(attribs.join(", "));
        }

        this._container.innerHTML = `
            <div class="attributes-body">${prefixAndAttribs.join(" | ")}</div>
            <div class="attributes-emblem">${this.options.emblem}</div>
        `;
    }
});

L.Map.mergeOptions({
    attributionControl: false,
    condensedAttributionControl: true
});

L.Map.addInitHook(function () {
    if (this.options.condensedAttributionControl) {
        new L.Control.CondensedAttribution().addTo(this);
    }
});

L.control.condensedAttribution = function (options) {
    return new L.Control.CondensedAttribution(options);
};
