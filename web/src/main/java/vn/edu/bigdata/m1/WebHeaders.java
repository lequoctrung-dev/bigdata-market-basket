package vn.edu.bigdata.m1;

import jakarta.servlet.*;
import jakarta.servlet.http.*;
import org.springframework.stereotype.Component;
import java.io.IOException;

@Component
public class WebHeaders implements Filter {
    @Override public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {
        HttpServletResponse r=(HttpServletResponse)response;
        r.setHeader("X-Content-Type-Options","nosniff");
        r.setHeader("Referrer-Policy","no-referrer");
        r.setHeader("Content-Security-Policy","default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'");
        chain.doFilter(request,response);
    }
}
