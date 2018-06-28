#version 330 core

out vec4 FragColor;

in vec2 texCoord;
in vec3 surfaceNormal;
in vec3 toLight;
in vec3 toCamera;

uniform float shineDamp;
uniform float reflectivity;
uniform vec3 lightColor;
uniform sampler2D textureSampler;

void main() {
    vec3 unitNormal = normalize(surfaceNormal);
    vec3 unitLight = normalize(toLight);

    float nDot1 = dot(unitNormal, unitLight);
    float brightness = max(nDot1, 0.2);
    vec3 diffuse = brightness * lightColor;

    vec3 unitCamera = normalize(toCamera);
    vec3 lightDirection = -unitLight;
    vec3 reflectDirection = reflect(lightDirection, unitNormal);

    float specularFactor = dot(reflectDirection, unitCamera);
    specularFactor = max(specularFactor, 0.0);
    float dampedFactor = pow(specularFactor, shineDamp);
    vec3 finalSpecular = dampedFactor * reflectivity *lightColor;

    FragColor = vec4(diffuse, 1.0) * texture(textureSampler, texCoord) + vec4(finalSpecular, 1.0);
}
