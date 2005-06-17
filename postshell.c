/*
 * Copyright (c) 2002 Michal Moskal <malekith@pld-linux.org>.
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
 *	This product includes software developed by Michal Moskal.
 * 4. Neither the name of the author nor the names of any co-contributors
 *    may be used to endorse or promote products derived from this software
 *    without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY MICHAL MOSKAL AND CONTRIBUTORS ``AS IS'' AND
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
 * This simple program is aimed to be used as script interpreter in rpm
 * %post scriptlets and the like. It opens file passed as first argument
 * and executes commands found there. Only linear execution is supported.
 * For example, in glibc.spec:
 *
 * %post -p /sbin/postshell
 * ldconfig
 * -telinit q
 *
 * (full patch like /sbin/ldconfig or -/sbin/tellinit will also work).
 *
 * If command starts with - its exit status is ignored. Otherwise last 
 * non-zero exit status is returned.
 *
 * There are no builtin commands (yet :).
 *
 * Following commands *will* work as expected (as in Bourne shell):
 *
 * /bin/echo "Foo     bar baz"
 * insmod foobar options="foo bar 'qux'"
 * false
 *
 * Following *won't*:
 *
 * exit 1
 * echo foo || echo baz
 * set -x
 * 
 * Patches and bugreports are welcome, direct them to Michal Moskal
 * <malekith@pld-linux.org>.
 */

#define _GNU_SOURCE
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE 1024
#define MAX_ARGS 32
#define SEARCH_PATH { "/sbin/", "/bin/", "/usr/sbin/", "/usr/bin/", NULL }

int exit_status;
int ignore_status;

void do_execve(char **argv)
{
	char *path[] = SEARCH_PATH;
	char file[MAX_LINE + 100];
	int i; 

	if (**argv == '.' || **argv == '/')
		execve(argv[0], argv, environ);
	else 
		for (i = 0; path[i]; i++) {
			strcpy(file, path[i]);
			strcat(file, argv[0]);
			execve(file, argv, environ);
		}
}

int exec_and_wait(char **argv)
{
	pid_t pid;

	pid = fork();

	if (pid == -1) {
		perror("fork");
		return -1;
	} else if (pid == 0) {
		/* child. */
		do_execve(argv);
		if (!ignore_status) 
			perror(argv[0]); 
		exit(127);
	} else {
		int status, err;
		
		err = waitpid(pid, &status, 0);
		if (err < 0) {
			perror("waitpid");
			return -1;
		} else
			return WEXITSTATUS(status);
	}
}

void split_argv(char **argv, char *s)
{
	char *dst;
	int argc, delim;
	
	for (argc = 0; argc < MAX_ARGS; argc++) {
		while (*s == ' ' || *s == '\t')
			s++;

		if (*s == 0)
			break;

		argv[argc] = s;
		dst = s;
		
		while (*s && *s != ' ' && *s != '\t') {
			if (*s == '\'' || *s == '"') {
				delim = *s++;
				while (*s && *s != delim)
					*dst++ = *s++;
				if (*s)
					s++;
			} else {
				*dst++ = *s++;
			}
		}

		if (*dst) {
			if (s == dst)
				s++;
			*dst++ = 0;
		}
	}

	argv[argc] = NULL;
}

void exec_line(char *s)
{
	char *argv[MAX_ARGS + 1];
	int ret;

	split_argv(argv, s);
	
	ignore_status = 0;

	if (**argv == '-') {
		ignore_status++;
		(*argv)++;
	}

	ret = exec_and_wait(argv);

	if (ret && !ignore_status)
		exit_status = ret;
}

void exec_file(FILE *f)
{
	char line[MAX_LINE];

	while (fgets(line, sizeof(line), f)) {
		/* chomp it */
		if (line[strlen(line) - 1] == '\n')
			line[strlen(line) - 1] = 0;
		/* and exec. */
		exec_line(line);
	}
}

#define error(msg) write(2, msg, strlen(msg))
int main(int argc, char **argv)
{
	FILE *f;

	if (argc < 2) {
		error("USAGE: ");
		error(argv[0]);
		error(" filename\n");
		exit(1);
	}

	f = fopen(argv[1], "r");
	
	if (f == NULL) {
		perror(argv[1]);
		exit(1);
	}

	exec_file(f);
	fclose(f);
	exit(exit_status);
}
