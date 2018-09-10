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
uniform vec3 skyColor;

uniform sampler2D bgTexture;
uniform sampler2D rTexture;
uniform sampler2D gTexture;
uniform sampler2D bTexture;
uniform sampler2D blendMap;

void main() {
    vec4 blendMapColor = texture(blendMap, texCoord);

    float bgTextureAmount = 1 - (blendMapColor.r + blendMapColor.g + blendMapColor.b);
    vec2 tiledCoords = texCoord * 40.0;
    vec4 bgTextureColor = texture(bgTexture, tiledCoords) * bgTextureAmount;
    vec4 rTextureColor = texture(rTexture, tiledCoords) * blendMapColor.r;
    vec4 gTextureColor = texture(gTexture, tiledCoords) * blendMapColor.g;
    vec4 bTextureColor = texture(bTexture, tiledCoords) * blendMapColor.b;

    vec4 totalColor = bgTextureColor + rTextureColor + gTextureColor + bTextureColor;

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

    FragColor = vec4(diffuse, 1.0) * totalColor + vec4(finalSpecular, 1.0);
    FragColor = mix(vec4(skyColor, 1.0), FragColor, visibility);
}
