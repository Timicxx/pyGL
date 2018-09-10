#version 330 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec2 texture_coord;
layout(location = 2) in vec3 normal;

out vec2 texCoord;
out vec3 surfaceNormal;
out vec3 toLight;
out vec3 toCamera;
out float visibility;

uniform vec3 lightPosition;
uniform mat4 model_matrix;
uniform mat4 view_matrix;
uniform mat4 projection_matrix;

const float density = 0.0035;
const float gradient = 5.0;

void main() {
    vec4 worldPos = vec4(position, 1.0) * model_matrix;
    vec4 positionRelativeToCamera = worldPos * view_matrix;

	gl_Position = positionRelativeToCamera * projection_matrix;
	texCoord = texture_coord;

	surfaceNormal = (vec4(normal, 0.0) * model_matrix).xyz;
	toLight = lightPosition - worldPos.xyz;
	toCamera = (inverse(view_matrix) * vec4(0.0, 0.0, 0.0, 1.0)).xyz - worldPos.xyz;

	float distance = length(positionRelativeToCamera.xyz);
	visibility = exp(-pow((distance*density), gradient));
	visibility = clamp(visibility, 0.0, 1.0);
}