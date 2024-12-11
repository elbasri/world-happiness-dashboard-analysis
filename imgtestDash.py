import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import tensorflow as tf
import numpy as np
import cv2
import base64
from io import BytesIO
from PIL import Image

# Load VGG16 model
model = tf.keras.applications.vgg16.VGG16()

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "CNN Visualization"

# Layout
app.layout = html.Div([
    html.H1("Visualizing Convolutional Layers in CNN"),

    html.Div([
        html.H3("Upload an Image"),
        dcc.Upload(
            id='upload-image',
            children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
            style={
                'width': '100%', 'height': '60px', 'lineHeight': '60px',
                'borderWidth': '1px', 'borderStyle': 'dashed',
                'borderRadius': '5px', 'textAlign': 'center', 'margin': '10px'
            },
            multiple=False
        ),
        html.Div(id='output-image-upload'),
    ]),

    html.Div([
        html.H3("Select a Convolutional Layer"),
        dcc.Dropdown(
            id='layer-dropdown',
            options=[
                {'label': layer.name, 'value': layer.name} 
                for layer in model.layers if 'conv' in layer.name
            ],
            value=model.layers[1].name
        ),
    ]),

    html.Div([
        html.H3("Visualized Filters"),
        dcc.Graph(id='filter-visualization')
    ]),

    html.Div([
        html.H3("Transformed Image"),
        dcc.Graph(id='transformed-image')
    ])
])

# Callbacks
@app.callback(
    Output('output-image-upload', 'children'),
    Input('upload-image', 'contents'),
)
def display_uploaded_image(contents):
    if contents:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        image = Image.open(BytesIO(decoded))
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        data = buffer.getvalue()
        img_base64 = base64.b64encode(data).decode()
        return html.Img(src='data:image/png;base64,' + img_base64, style={'height': '200px'})
    return None

@app.callback(
    Output('filter-visualization', 'figure'),
    Input('layer-dropdown', 'value')
)
def visualize_filters(layer_name):
    layer = next(layer for layer in model.layers if layer.name == layer_name)
    filters, biases = layer.get_weights()
    num_filters = filters.shape[-1]
    
    # Normalize filter values to 0-1
    f_min, f_max = filters.min(), filters.max()
    filters = (filters - f_min) / (f_max - f_min)

    # Visualize the first 6 filters
    fig = px.imshow(np.concatenate([filters[:, :, :, i] for i in range(6)], axis=1),
                    facet_col=0, binary_string=True)
    fig.update_layout(title=f"Filters in Layer {layer_name}")
    return fig

@app.callback(
    Output('transformed-image', 'figure'),
    [Input('upload-image', 'contents'),
     Input('layer-dropdown', 'value')]
)
def visualize_transformed_image(contents, layer_name):
    if not contents:
        return px.imshow(np.zeros((224, 224, 3)), title="Upload an image to view transformations")

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    image = Image.open(BytesIO(decoded))
    image = image.resize((224, 224))
    image_array = np.array(image) / 255.0

    # Prepare image for model
    image_array = np.expand_dims(image_array, axis=0)
    
    # Redefine model
    layer_output = model.get_layer(layer_name).output
    intermediate_model = tf.keras.models.Model(inputs=model.input, outputs=layer_output)
    transformed_image = intermediate_model.predict(image_array)[0]
    
    # Visualize
    fig = px.imshow(transformed_image.mean(axis=-1), title="Transformed Image")
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
