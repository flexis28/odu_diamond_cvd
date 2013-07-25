import std.stdio;

void comp(double a, double b) {
  write(a, " < ", b, " ");
  if (a < b) writeln("true");
  else writeln("false");
}

void main() {
  comp(1.0, 100.0);
  comp(1.0, float.init);
  comp(float.init, 100.0);
  comp(float.init , float.init);
}