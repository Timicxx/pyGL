#version 330 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec2 texture_coord;
layout(location = 2) in vec3 normal;

out vec2 texCoord;
out vec3 surfaceNormal;
out vec3 toLight;
out vec3 toCamera;

uniform vec3 lightPosition;
uniform mat4 model_matrix;
uniform mat4 view_matrix;
uniform mat4 projection_matrix;
uniform float useFakeLightning;

void main() {
    vec4 worldPos = vec4(position, 1.0) * model_matrix;
	gl_Position = worldPos * view_matrix * projection_matrix;
	texCoord = texture_coord;

	vec3 actualNormal = normal;
    if(useFakeLightning > 0.5){
        actualNormal = vec3(0.0, 1.0, 0.0);
    }

	surfaceNormal = (vec4(actualNormal, 0.0) * model_matrix).xyz;
	toLight = lightPosition - worldPos.xyz;
	toCamera = (inverse(view_matrix) * vec4(0.0, 0.0, 0.0, 1.0)).xyz - worldPos.xyz;
}