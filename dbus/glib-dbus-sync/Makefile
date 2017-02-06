interface_xml :=value-dbus-interface.xml

pkg_packages := dbus-1 dbus-glib-1

PKG_CFLAGS :=$(shell pkg-config --cflags $(pkg_packages))
PKG_LDFLAGS :=$(shell pkg-config --libs $(pkg_packages))

ADD_CFALGS := -g -Wall -DG_DISABLE_DEPRECATED
ADD_CFLAGS += -DNO_DAEMON

# Combine flags
CFLAGS := $(PKG_CFLAGS) $(ADD_CFALGS) $(CFLAGS)
LDFLAGS := $(PKG_LDFLAGS) $(LDFLAGS)

cleanfiles := value-client-stub.h \
    value-server-stub.h

targets = server client
.PHONY: all clean checkxml
all: $(targets)

server: server.o
	$(CC) $^ -o $@ $(LDFLAGS)
client: client.o
	$(CC) $^ -o $@ $(LDFLAGS)

server.o: server.c common-defs.h value-server-stub.h
	$(CC) $(CFLAGS) -DPROGNAME=\"$(basename $@)\" -c $< -o $@
client.o: client.c common-defs.h value-client-stub.h
	$(CC) $(CFLAGS) -DPROGNAME=\"$(basename $@)\" -c $< -o $@

value-server-stub.h: $(interface_xml)
	dbus-binding-tool --prefix=value_object --mode=glib-server \
    $< > $@
value-client-stub.h: $(interface_xml)
	dbus-binding-tool --prefix=value_object --mode=glib-client \
    $< > $@

checkxml: $(interface_xml)
	@xmllint --valid --noout $<
	@echo $< checks out ok

clean:
	$(RM) $(targets) $(cleanfiles) *.o

server.o client.o: Makefile