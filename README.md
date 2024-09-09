<h1>Pivot</h1>

## Inspirations

- [Fulcrum](https://github.com/dschil138/Fulcrum)
5-Way switch and joystick.
- [Scotto34](https://github.com/joe-scotto/scottokeebs/tree/main/Scotto34/Handwired/Case)
General case design.
- [Paintbrush](https://github.com/artseyio/thepaintbrush)
Low key-count, sans column-stagger and splay.

> [!IMPORTANT]  
> The Fulcrum README is very pretty, and I might shamelessly remix it once my
> board is actually done -- consider this WIP.

## Cloning and Authenticating

``` bash
git clone 'https://github.com/antler5/Pivot' && cd Pivot
```

You may verify that each commit in this branch has been signed by an
authorized contributer via GNU Guix's
[authentication](https://guix.gnu.org/manual/en/html_node/Invoking-guix-git-authenticate.html)
mechanism.

``` bash
git fetch keyring keyring:keyring
guix git authenticate \
  'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' \
  'DACB 035F B9B0 EE9C 7E13  1AAA C310 15D9 6620 A955'
```

## License

GPL-3.0-only
