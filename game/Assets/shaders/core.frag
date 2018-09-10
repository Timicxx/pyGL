#version 330 core

out vec4 FragColor;

in vec2 texCoord;
in vec3 surfaceNormal;
in vec3 toLight;
in vec3 toCamera;
in float visibility;

uniform float shineDamp;
uniform float reflectivity;
uniform vec3 lightColor;
uniform sampler2D textureSampler;
uniform vec3 skyColor;

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

    vec4 texColor = texture(textureSampler, texCoord);
    if(texColor.a < 0.5f){
        discard;
    }

    FragColor = vec4(diffuse, 1.0) * texColor + vec4(finalSpecular, 1.0);
    FragColor = mix(vec4(skyColor, 1.0), FragColor, visibility);
}
