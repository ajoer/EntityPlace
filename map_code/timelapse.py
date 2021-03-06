import map_code.map_visualization as mv
import pandas as pd
import plotly.graph_objects as go

class Timelapse:

    def __init__(self, event, language, focus, visualize_month=False, show=False):
        v = mv.Visualize(event, language, focus)
        input_data = v.data

        self.months = list(input_data.keys())
        self.start_month = self.months[0]

        self.focus = v.focus
        if self.focus == "entity":
            self.entity_types = v.types
            self.month_data = self._get_entity_monthsplit_data(input_data)
        if self.focus == "location":
            self.month_data = input_data #self._get_location_monthsplit_data(input_data)
        self.fig_dict, self.sliders_dict = self._setup_fig_slider_dicts()
        self._make_frames()
        self._update_fig_dict()
        self.fig = go.Figure(self.fig_dict)
        if show == True:
            self.fig.show()

    def _get_entity_monthsplit_data(self, visualization_data):
        # split the data this way:
        # each month has a dictionary, where each key is a type (e.g. "Country") with its corresponding entities (e.g. "Iraq")
        # this is needed for the animation visualization. 

        month_types_dict = {}
        for month in self.months:
            month_dict = {}
            for entity_type in self.entity_types:
                type_dict = {  
                    "entities": [],
                    "latitudes": [],
                    "longitudes": [],
                    "frequencies": []
                }
                if entity_type in visualization_data[month]["entity_types"]:
                    indices = [i for i, x in enumerate(visualization_data[month]["entity_types"]) if x == entity_type]
                    for indx in indices:
                    
                        type_dict["entities"].append(visualization_data[month]["entities"][indx])
                        type_dict["latitudes"].append(visualization_data[month]["latitudes"][indx])
                        type_dict["longitudes"].append(visualization_data[month]["longitudes"][indx])
                        type_dict["frequencies"].append(visualization_data[month]["frequencies"][indx])

                if len(type_dict["entities"]) < 1: continue
                month_dict[entity_type] = type_dict
            month_types_dict[month] = month_dict
        return month_types_dict

    def _get_location_monthsplit_data(self, visualization_data):
        # split the data this way:
        # each month has a dictionary, where each key is a location (e.g. "Saudi Arabia") with its corresponding entities (e.g. "Main square")
        # this is needed for the animation visualization. 

        month_locations_dict = {}
        for month in self.months:
            month_dict = {}
            for location in locations:
                type_dict = {  
                    "entities": [],
                    "latitudes": [],
                    "longitudes": [],
                    "frequencies": []
                }
                if entity_type in visualization_data[month]["entity_types"]:
                    indices = [i for i, x in enumerate(visualization_data[month]["entity_types"]) if x == entity_type]
                    for indx in indices:
                    
                        type_dict["entities"].append(visualization_data[month]["entities"][indx])
                        type_dict["latitudes"].append(visualization_data[month]["latitudes"][indx])
                        type_dict["longitudes"].append(visualization_data[month]["longitudes"][indx])
                        type_dict["frequencies"].append(visualization_data[month]["frequencies"][indx])

                if len(type_dict["entities"]) < 1: continue
                month_dict[entity_type] = type_dict
            month_types_dict[month] = month_dict
        return month_types_dict

    def _setup_fig_slider_dicts(self):
        fig_dict = {
            "data": [],
            "layout": {},
            "frames": []
        }

        fig_dict["layout"]["width"] = 1400
        fig_dict["layout"]["height"] = 900
        fig_dict["layout"]["autosize"] = False
        fig_dict["layout"]["hovermode"] = "closest"
        fig_dict["layout"]["margin"] = {"l": 200,"t": 0,"b": 0,"r": 300}
        fig_dict["layout"]["mapbox"] = {
                "style": "stamen-terrain",
                "center": {"lon": 15, "lat": 18},
        		"zoom": 1
        	}
        fig_dict["layout"]["sliders"] = {
            "args": [
                "transition", {
                    "duration": 0,
                    "easing": "cubic-in-out"
                }
            ],
            "initialValue": self.start_month,
            "plotlycommand": "animate",
            "values": self.months,
            "visible": True
        }

        sliders_dict = {
        	"steps": [], 
            "transition": {"duration": 0},
            "x": 0.02,
            "y": 0, 
            "currentvalue": {
           		"font": {"size": 20},
           		"prefix": "Month: ", 
                "visible": True, 
                "xanchor": "right"
            },  
            "len": 0.96
        }
        return fig_dict, sliders_dict

    # # ------ FRAMES and DATA --------

    def _make_frames(self):

        prev_month_frame = {"data": {}, "name": str()}
        for n,month in enumerate(self.months):
            frame = {"data": [], "name": str(month)}

            if self.focus == "entity":
                for entity_type in sorted(self.entity_types):
                    if entity_type not in self.month_data[month]:
                        data_dict = {
                            "type": 'scattermapbox',
                            "mode": "markers",
                            "lat": [0.0],
                            "lon": [0.0],
                            "text": [],
                            "showlegend": True,
                            "opacity": 0,
                            "marker": {
                                "size": 2
                            },
                        }
                    else:
                        data_dict = {
                            "type": 'scattermapbox',
                            "mode": "markers",
                            "lat": self.month_data[month][entity_type]["latitudes"],
                            "lon": self.month_data[month][entity_type]["longitudes"],
                            "text": self.month_data[month][entity_type]["entities"],
                            "marker": {
                                "size": self.month_data[month][entity_type]["frequencies"]
                            },
                        }
                    data_dict["name"] = entity_type
                    frame["data"].append(data_dict)    

                    # month_0 is also the input for the start map, which can be animated by pressing "play"
                    if n == 0:
                        self.fig_dict["data"].append(data_dict)

            if self.focus == "location":
                for m, location in enumerate(self.month_data[month]["locations"]):
                    data_dict = {
                            "type": 'scattermapbox',
                            "mode": "markers",
                            "lat": [self.month_data[month]["latitudes"][m]],
                            "lon": [self.month_data[month]["longitudes"][m]],
                            #"text": location,
                            "marker": {
                                "color": 1,
                                "size": self.month_data[month]["frequencies"][m]
                            },
                        } 
                    data_dict["name"] = location
                    frame["data"].append(data_dict)    

                    # month_0 is also the input for the start map, which can be animated by pressing "play"
                    if n == 0:
                        self.fig_dict["data"].append(data_dict)

            # Filter out months without changes
            if prev_month_frame["data"] == frame["data"]: continue

            self.fig_dict["frames"].append(frame)
            
            prev_month_frame = frame

            slider_step = {"args": [
            	[month],
            	{"frame": {"duration": 40, "redraw": True},
            	"mode": "immediate",
            	"transition": {"duration": 0}}
            ],
            	"label": month,
            	"method": "animate"}
            self.sliders_dict["steps"].append(slider_step)

    def _update_fig_dict(self):
        self.fig_dict["layout"]["sliders"] = [self.sliders_dict]
        if self.focus == "entity":
            self.fig_dict["layout"]["legend"] = {
                    "title": {"text": "Entity types"},
                    "y": 0.5
            }
        # if self.focus == "location":
        #     self.fig_dict["layout"]["legend"] = {
        #             "title": {"text": "Locations"},
        #             "y": 0.5
        #     }
        self.fig_dict["layout"]["updatemenus"] = [
            {
                "buttons": [{
        			"args": [None, {"frame": {"duration": 100, "redraw": True},
                            "fromcurrent": True, 
                            "transition": {"duration": 0,
                            "easing": "quadratic-in-out"}}],
                    "label": "Play",
                    "method": "animate"
                    },
                    {
                    "args": [[None], {"frame": {"duration": 0, "redraw": True},
                            "mode": "immediate",
                            "transition": {"duration": 0}}],
                    "label": "Pause",
                    "method": "animate"
                    }
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 87},
                "showactive": True,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "right",
                "y": -0.2,
                "yanchor": "top"
        	}
        ]
