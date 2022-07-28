#version 430
in vec4 in_vert;
in vec4 in_col;
out vec4 v_color;
void main()
{
    gl_Position=in_vert;// x, y, 0, radius
    v_color=in_col;
}