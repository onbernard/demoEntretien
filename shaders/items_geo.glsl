#version 330
layout(points)in;
layout(triangle_strip,max_vertices=4)out;
in vec4 v_color[];
out vec2 uv;
out vec4 color;
void main(){
    float radius=gl_in[0].gl_Position.w;
    vec2 pos=gl_in[0].gl_Position.xy;
    // Emit the triangle strip creating a "quad"
    // Lower left
    gl_Position=vec4(pos+vec2(-radius,-radius),0,1);
    color=v_color[0];
    uv=vec2(0,0);
    EmitVertex();
    // upper left
    gl_Position=vec4(pos+vec2(-radius,radius),0,1);
    color=v_color[0];
    uv=vec2(0,1);
    EmitVertex();
    // lower right
    gl_Position=vec4(pos+vec2(radius,-radius),0,1);
    color=v_color[0];
    uv=vec2(1,0);
    EmitVertex();
    // upper right
    gl_Position=vec4(pos+vec2(radius,radius),0,1);
    color=v_color[0];
    uv=vec2(1,1);
    EmitVertex();
    EndPrimitive();
}