#version 430

#define MAX_ACC .01
#define MAX_VEL .005

#define GROUP_SIZE %COMPUTE_SIZE%
layout(local_size_x=GROUP_SIZE) in;
// All values are vec4s because of block alignment rules (keep it simple).
// We could also declare all values as floats to make it tightly packed.
// See : https://www.khronos.org/opengl/wiki/Interface_Block_(GLSL)#Memory_layout
struct Ball
{
    vec4 pos; // x, y, 0, radius
    vec4 vel; // x, y (velocity)
    vec4 col; // r, g, b (color)
};
layout(std430, binding=0) buffer balls_in
{
    Ball balls[];
} In;
layout(std430, binding=1) buffer balls_out
{
    Ball balls[];
} Out;

uniform float coef_r1;
uniform float coef_r2;
uniform float coef_r3;

void main()
{
    int x = int(gl_GlobalInvocationID);
    Ball in_ball = In.balls[x];
    vec4 p = in_ball.pos.xyzw;
    vec4 v = in_ball.vel.xyzw;
    
    vec2 com = vec2(0.);
    for(int i=0; i<256; i++) {
        if(i != x) {
            com += (In.balls[i].pos.xy);
        }
    }
    com = com/(255.);
    vec2 rule1 = vec2((com-p.xy)/100);

    vec2 rule2 = vec2(0.);
    for(int i=0; i<256; i++){
        if(i != x) {
            vec2 dir = In.balls[i].pos.xy - p.xy;
            rule2 -= normalize(dir)/(1.+dot(dir,dir));
        }
    }
    rule2 /= 100.;

    vec2 cov = vec2(0.);
    for(int i=0; i<256; i++) {
        if(i != x) {
            cov += (In.balls[i].vel.xy);
        }
    }
    cov = cov/255.;
    vec2 rule3 = cov-v.xy;

    vec2 acc = coef_r1*rule1 + coef_r2*rule2/100. + coef_r3*rule3/100.;
    float norm_acc = min(length(acc), MAX_ACC);
    v += vec4(normalize(acc)*norm_acc, 0., 0.);
    float norm_vel = min(length(v), MAX_VEL);
    p += normalize(v)*norm_vel;

    float rad = p.w * 0.5;
    if (p.x - rad <= -1.0)
    {
        p.x = -1.0 + rad;
        v.x *= -0.98;
    }
    else if (p.x + rad >= 1.0)
    {
        p.x = 1.0 - rad;
        v.x *= -0.98;
    }
    if (p.y - rad <= -1.0)
    {
        p.y = -1.0 + rad;
        v.y *= -0.98;
    }
    else if (p.y + rad >= 1.0)
    {
        p.y = 1.0 - rad;
        v.y *= -0.98;
    }

    Ball out_ball;
    out_ball.pos.xyzw = p.xyzw;
    out_ball.vel.xyzw = v.xyzw;
    vec4 c = in_ball.col.xyzw;
    out_ball.col.xyzw = c.xyzw;
    Out.balls[x] = out_ball;
}