/*
 * Copyright (c) 2004, 2005 Elan Ruusamäe <glen@pld-linux.org>.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. All advertising materials mentioning features or use of this software
 *    must display the following acknowledgement:
 *	  This product includes software developed by Elan Ruusamäe
 * 4. Neither the name of the author nor the names of any co-contributors
 *    may be used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY ELAN RUUSAMÄE AND CONTRIBUTORS ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 */

/*
 * Usage
 * ~~~~~
 *
 * This simple program is aimed to be used as a workaround when installing over
 * glibc which has placed glibc.so into /lib/i686.
 *
 * For example, in glibc.spec:
 *
 * %post -p /sbin/postshell
 * /sbin/glibc-postinst /%{_lib}/%{_host_cpu}
 * /sbin/ldconfig /%{_lib} %{_prefix}/%{_lib}
 *
 * Patches and bugreports are welcome, direct them to Elan Ruusamäe
 * <glen@pld-linux.org>.
 */


#include <sys/stat.h>
#include <unistd.h>
#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <stdlib.h>

#define error(msg) write(2, msg, strlen(msg))
#define warn(msg) write(2, msg, strlen(msg))

int main (int argc, char *argv[])
{
struct stat st;
int i, rv = 0;

	if (argc == 1) {
		error("This program is intended to be used by glibc postinstall stage.\n");
		exit(1);
	}

	for (i = 1; i < argc; i++) {
		char *path = argv[i];

		if (stat(path, &st) == -1) {
			// doesn't exist. good. next please.
			if (errno == ENOENT) {
				continue;
			}
			perror("stat");
			exit(1);
		}

		if (S_ISDIR(st.st_mode)) {
			int l = strlen(path);
			char p[l + sizeof(".rpmsave") + 1];

			strcpy(p, path);
			strcpy(p + l, ".rpmsave");
			warn("Renaming "); warn(path); warn(" to "); warn(p); warn("\n");
			if (rename(path, p) == -1) {
				perror("rename");
				rv = 1;
			}
		}
	}

	exit(rv);
}
