<template>
    <div ref="map-root" style="width: 100%; height: 100%"></div>
</template>

<script>
import View from 'ol/View';
import Map from 'ol/Map';
import TileLayer from 'ol/layer/Tile';
import 'ol/ol.css';
import { toLonLat } from 'ol/proj';
import { iso1A2Code } from '@rapideditor/country-coder';
import * as geoJson from 'world-geojson';
import countryCodeData from '../assets/countryCodes.json';
import VectorLayer from 'ol/layer/Vector';
import VectorSource from 'ol/source/Vector';
import GeoJSON from 'ol/format/GeoJSON';
import Style from 'ol/style/Style';
import Fill from 'ol/style/Fill';
import Stroke from 'ol/style/Stroke';
import StadiaMaps from 'ol/source/StadiaMaps.js';

export default {
  name: 'MapContainer',
  data() {
    return {
      currentCountryLayer: null,
      currentCountryCode: null,
      map: null
    };
  },
  mounted() {
    // Create the OpenLayers map
    this.map = new Map({
      target: this.$refs['map-root'],
      layers: [
        new TileLayer({
          source: new StadiaMaps({
            layer: 'stamen_toner_lite',
          }), // Sets the style of the map
        }),
      ],

      // Ensures that the map is centered and not zoomed on load
      view: new View({
        zoom: 0,
        center: [0, 0],
        constrainResolution: true,
      }),
    });


    // Add a click event listener to the map
    this.map.on('click', (event) => {
      
      const point = this.map.getCoordinateFromPixel(event.pixel);

      // Convert the coordinates from the map's projection to longitude and latitude
      const lonLat = toLonLat(point);

      // Translate coordinates to country acronym
      let country_code = iso1A2Code(lonLat);
      this.currentCountryCode = country_code;
      // Emits an event to the parent that a new country has been selected and send what the selection is
      this.$emit('country-selected', this.currentCountryCode);

      // Convert country acronym to country name
      let country_name = countryCodeData[country_code];
      if (country_name) {

        // Clear the previous vector layer if it exists
        if (this.currentCountryLayer) {
            this.map.removeLayer(this.currentCountryLayer);
        }

        // Get the GeoJSON polygon data for the country
        let country_polygon = geoJson.forCountry(country_name);
        
        // Create a vector source with the GeoJSON polygon data
        const vectorSource = new VectorSource({
          features: new GeoJSON().readFeatures(country_polygon, {
            dataProjection: 'EPSG:4326',
            featureProjection: this.map.getView().getProjection(),
          }),
        });

        // Create a vector layer using the vector source
        const vectorLayer = new VectorLayer({
          source: vectorSource,
          style: new Style({
            fill: new Fill({
              color: "rgba(108,255,143,0.5)",
            }),
            stroke: new Stroke({
              color: '#008f22',
              width: 2,
            }),
          }),
        });

        // Update the reference to the current country layer
        this.currentCountryLayer = vectorLayer;
        
        // Add the vector layer to the map
        this.map.addLayer(this.currentCountryLayer);
      }
    });
  },
  methods: {
    resetMap() {
      if (this.currentCountryLayer) {
        // Remove old polygon if one exists
        this.map.removeLayer(this.currentCountryLayer);
      }
      //Reset varibles for front-end guess 
      this.currentCountryCode = null
      this.currentCountryCode = null
    } 
  }
};
</script>

  